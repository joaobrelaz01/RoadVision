#!/usr/bin/env python3
"""
scripts/feed_roadvision_ci.py
Pipeline de AutomaÃ§Ã£o ContÃ­nua e AlimentaÃ§Ã£o de Dados RoadVision (CI/CD).
Simula a curva diurna litorÃ¢nea real da SP-055 (Rio-Santos), gera contagens
realistas ponderadas por dia da semana e horÃ¡rio (America/Sao_Paulo),
insere em contagens_minuto e contagens_por_sentido, e atualiza o Supabase Storage.

Uso:
    python scripts/feed_roadvision_ci.py [--dry-run]
"""
import os
import sys
import argparse
import random
import zoneinfo
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

# Carrega variÃ¡veis de ambiente do .env se existir
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

from backend.app.database.supabase_client import get_supabase

TZ_SP = zoneinfo.ZoneInfo("America/Sao_Paulo")
SAMPLE_DIR = BASE_DIR / "assets" / "sample_captures"


def calcular_perfil_diurno_sp055(dt_sp: datetime) -> Tuple[float, Dict[str, float], float]:
    """
    Retorna o multiplicador de fluxo da SP-055 e a divisÃ£o direcional
    para o momento atual (hora e dia da semana em BrasÃ­lia).
    
    Retorna:
        - multiplicador de volume (0.0 a 2.5)
        - proporÃ§Ã£o por sentido (ex: {"Ubatuba": 0.7, "Maranduba": 0.3})
        - velocidade mÃ©dia estimada (km/h)
    """
    dia_semana = dt_sp.weekday()  # 0=Segunda, ..., 4=Sexta, 5=SÃ¡bado, 6=Domingo
    hora = dt_sp.hour + (dt_sp.minute / 60.0)

    # 1. Curva base horÃ¡ria
    if 0 <= hora < 5:
        # Madrugada: trÃ¡fego muito baixo
        fator_base = 0.15 + (hora / 5.0) * 0.15
        sentido_prop = {"Ubatuba": 0.50, "Maranduba": 0.50}
        velocidade = random.uniform(75.0, 85.0)
    elif 5 <= hora < 9:
        # ManhÃ£: pico comercial matutino
        pico = 1.0 - abs(hora - 7.5) / 2.0
        fator_base = 0.5 + max(0.0, pico) * 0.8
        sentido_prop = {"Ubatuba": 0.52, "Maranduba": 0.48}
        velocidade = random.uniform(60.0, 72.0)
    elif 9 <= hora < 16:
        # Meio do dia: fluxo estÃ¡vel comercial/turÃ­stico
        fator_base = 0.75 + random.uniform(-0.1, 0.1)
        sentido_prop = {"Ubatuba": 0.50, "Maranduba": 0.50}
        velocidade = random.uniform(65.0, 75.0)
    elif 16 <= hora < 20:
        # Fim de tarde: pico vespertino
        pico = 1.0 - abs(hora - 18.0) / 2.0
        fator_base = 0.8 + max(0.0, pico) * 1.0
        sentido_prop = {"Ubatuba": 0.48, "Maranduba": 0.52}
        velocidade = random.uniform(55.0, 68.0)
    else:
        # Noite: declÃ­nio progressivo
        fator_base = 0.5 - ((hora - 20) / 4.0) * 0.3
        sentido_prop = {"Ubatuba": 0.50, "Maranduba": 0.50}
        velocidade = random.uniform(70.0, 80.0)

    # 2. Modificadores sazonais de fim de semana litorÃ¢neo (SP-055)
    if dia_semana == 4:  # Sexta-feira
        if hora >= 15:
            # Descida pesada para as praias do Litoral Norte
            fator_base *= 1.45
            sentido_prop = {"Ubatuba": 0.72, "Maranduba": 0.28}
            velocidade = max(45.0, velocidade - 15.0)
    elif dia_semana == 5:  # SÃ¡bado
        if 8 <= hora <= 13:
            # Chegada de turistas pela manhÃ£
            fator_base *= 1.35
            sentido_prop = {"Ubatuba": 0.65, "Maranduba": 0.35}
            velocidade = max(50.0, velocidade - 10.0)
    elif dia_semana == 6:  # Domingo
        if 14 <= hora <= 22:
            # Retorno em massa para a capital/Vale
            fator_base *= 1.60
            sentido_prop = {"Ubatuba": 0.25, "Maranduba": 0.75}
            velocidade = max(40.0, velocidade - 20.0)

    return fator_base, sentido_prop, round(velocidade, 1)


def gerar_contagens_veiculos(fator_volume: float) -> Dict[str, int]:
    """
    Gera volume de veÃ­culos proporcional ao fator da curva.
    Volume base por minuto: ~5 a 15 veÃ­culos em fluxo normal.
    """
    total_veiculos = max(2, int(random.gauss(10, 2) * fator_volume))

    # ComposiÃ§Ã£o tÃ­pica rodoviÃ¡ria litorÃ¢nea SP:
    # Carros ~72%, Motos ~14%, CaminhÃµes ~10%, Ã”nibus ~4%
    n_carros = int(total_veiculos * random.uniform(0.68, 0.75))
    sobra = max(0, total_veiculos - n_carros)
    
    n_motos = int(sobra * random.uniform(0.40, 0.55))
    sobra = max(0, sobra - n_motos)
    
    n_caminhoes = int(sobra * random.uniform(0.50, 0.75))
    n_onibus = max(0, sobra - n_caminhoes)

    # Garante que a soma bate exatamente com total_veiculos
    diff = total_veiculos - (n_carros + n_motos + n_onibus + n_caminhoes)
    n_carros += diff

    return {
        "carros": max(0, n_carros),
        "motos": max(0, n_motos),
        "onibus": max(0, n_onibus),
        "caminhoes": max(0, n_caminhoes),
    }


def sincronizar_storage(client, dry_run: bool = False) -> str:
    """
    Garante a existÃªncia do bucket 'camera-captures' e realiza upload
    de imagens reais de amostra.
    """
    if dry_run or not client:
        return "[DRY-RUN] Upload simulado de latest.jpg e camera_36.jpg para bucket 'camera-captures'"

    try:
        # Verifica se bucket existe
        buckets = client.storage.list_buckets()
        bucket_names = [b.name if hasattr(b, 'name') else b.get('name') for b in buckets]
        if "camera-captures" not in bucket_names:
            try:
                client.storage.create_bucket("camera-captures", options={"public": True})
                print("[Storage] Bucket 'camera-captures' criado com sucesso.")
            except Exception as e:
                print(f"[Storage] Nota ao criar bucket: {e}")

        # Realiza upload de latest.jpg e camera_36.jpg se existirem
        for f_name in ["latest.jpg", "camera_36.jpg"]:
            f_path = SAMPLE_DIR / f_name
            if f_path.exists():
                with open(f_path, "rb") as f:
                    file_bytes = f.read()
                try:
                    client.storage.from_("camera-captures").upload(
                        path=f_name,
                        file=file_bytes,
                        file_options={"content-type": "image/jpeg", "upsert": "true"}
                    )
                    print(f"[Storage] Upload de {f_name} realizado com sucesso.")
                except Exception as ue:
                    print(f"[Storage] Nota no upload de {f_name}: {ue}")

        return "Upload para Supabase Storage finalizado."
    except Exception as e:
        return f"[Storage] Erro ao sincronizar storage: {e}"


def main():
    parser = argparse.ArgumentParser(description="Pipeline de AlimentaÃ§Ã£o ContÃ­nua RoadVision (CI/CD)")
    parser.add_argument("--dry-run", action="store_true", help="Executa simulaÃ§Ã£o completa sem gravar no banco de dados")
    args = parser.parse_args()

    agora_sp = datetime.now(TZ_SP)
    agora_utc = agora_sp.astimezone(timezone.utc).isoformat()
    print(f"=== RoadVision Continuous Feed Pipeline ===")
    print(f"Data/Hora Local: {agora_sp.strftime('%d/%m/%Y %H:%M:%S')} ({TZ_SP})")
    print(f"Data/Hora UTC:   {agora_utc}")
    print(f"Modo de ExecuÃ§Ã£o: {'[DRY-RUN - Apenas SimulaÃ§Ã£o]' if args.dry_run else '[LIVE - Escrita em Supabase]'}")

    fator_vol, proporcoes_sentido, vel_media = calcular_perfil_diurno_sp055(agora_sp)
    print(f"Perfil Diurno SP-055: Fator de volume={fator_vol:.2f} | Velocidade={vel_media} km/h")
    print(f"DistribuiÃ§Ã£o de Sentidos: {proporcoes_sentido}")

    # Consulta cÃ¢meras ativas cadastradas no Supabase
    client = get_supabase()
    cameras_db = []
    if client:
        try:
            res = client.table("cameras").select("id, nome, km, ativa").execute()
            cameras_db = res.data or []
        except Exception as e:
            print(f"[Aviso] Falha ao consultar cÃ¢meras do Supabase: {e}")

    # CÃ¢meras alvo (se nÃ£o houver banco conectado, usa IDs conhecidos para dry-run)
    if not cameras_db:
        cameras_db = [
            {"id": "aa708460-ea62-48f2-b924-e5e058e3ed89", "nome": "DER SP - Camera 36", "km": "055+000", "camera_der_id": 36},
            {"id": "5144fc7b-a590-4de3-b338-700bda1ef368", "nome": "DER SP - Camera 14", "km": "211+000", "camera_der_id": 14}
        ]

    print(f"CÃ¢meras identificadas para alimentaÃ§Ã£o: {len(cameras_db)}")

    payload_minuto = []
    payload_sentido = []

    for cam in cameras_db:
        cam_id = cam["id"]
        cam_nome = cam.get("nome", f"Camera {cam_id}")

        contagem = gerar_contagens_veiculos(fator_vol)

        row_minuto = {
            "camera_id": cam_id,
            "data_hora": agora_utc,
            "carros": contagem["carros"],
            "motos": contagem["motos"],
            "onibus": contagem["onibus"],
            "caminhoes": contagem["caminhoes"],
        }
        payload_minuto.append(row_minuto)

        # DivisÃ£o por sentido (ex: Ubatuba e Maranduba)
        for sentido, prop in proporcoes_sentido.items():
            row_sentido = {
                "camera_id": cam_id,
                "data_hora": agora_utc,
                "sentido": sentido,
                "carros": max(0, int(contagem["carros"] * prop)),
                "motos": max(0, int(contagem["motos"] * prop)),
                "onibus": max(0, int(contagem["onibus"] * prop)),
                "caminhoes": max(0, int(contagem["caminhoes"] * prop))
            }
            payload_sentido.append(row_sentido)

        print(f"  -> {cam_nome}: Total={(contagem['carros'] + contagem['motos'] + contagem['onibus'] + contagem['caminhoes'])} veÃ­c "
              f"(Carros={contagem['carros']}, Motos={contagem['motos']}, "
              f"Ã”nibus={contagem['onibus']}, CaminhÃµes={contagem['caminhoes']})")

    # InserÃ§Ãµes no Supabase
    if args.dry_run:
        print("\n[DRY-RUN] Nenhuma gravaÃ§Ã£o executada no Supabase.")
        print(f"[DRY-RUN] Registros contagens_minuto gerados: {len(payload_minuto)}")
        print(f"[DRY-RUN] Registros contagens_por_sentido gerados: {len(payload_sentido)}")
        storage_status = sincronizar_storage(client, dry_run=True)
        print(f"[DRY-RUN] {storage_status}")
    else:
        if not client:
            print("[ERRO] Supabase nÃ£o estÃ¡ configurado. Abortando gravaÃ§Ã£o.")
            sys.exit(1)

        try:
            res_m = client.table("contagens_minuto").insert(payload_minuto).execute()
            print(f"[Banco] {len(payload_minuto)} registros inseridos em contagens_minuto.")
        except Exception as e:
            print(f"[ERRO] Falha ao inserir em contagens_minuto: {e}")

        try:
            res_s = client.table("contagens_por_sentido").insert(payload_sentido).execute()
            print(f"[Banco] {len(payload_sentido)} registros inseridos em contagens_por_sentido.")
        except Exception as e:
            print(f"[ERRO] Falha ao inserir em contagens_por_sentido: {e}")

        storage_res = sincronizar_storage(client, dry_run=False)
        print(f"[Storage] {storage_res}")

    print("=== Pipeline executado com sucesso. ===")


if __name__ == "__main__":
    main()


