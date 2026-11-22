#!/usr/bin/env python3
"""
scripts/feed_roadvision_ci.py
Pipeline de Automação Contínua e Alimentação de Dados RoadVision (CI/CD).
Simula a curva diurna litorânea real da SP-055 (Rio-Santos) com sazonalidade
por data, dia da semana, feriados (SP/Nacionais), perfil individual por câmera
e continuidade temporal entre leituras de 5 minutos.

Uso:
    python scripts/feed_roadvision_ci.py [--dry-run]
"""
import os
import sys
import math
import hashlib
import argparse
import random
import zoneinfo
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from typing import Dict, Any, List, Tuple, Optional

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


def _gaussiana(x: float, centro: float, largura: float) -> float:
    return math.exp(-0.5 * ((x - centro) / largura) ** 2)


def _calcular_pascoa(ano: int) -> date:
    """Algoritmo de Meeus/Jones/Butcher para data da Páscoa."""
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(ano, mes, dia)


def obter_feriados_sp(ano: int) -> set:
    """Retorna conjunto de datas de feriados nacionais e estaduais (SP)."""
    pascoa = _calcular_pascoa(ano)
    moveis = {
        pascoa - timedelta(days=48),  # Segunda de Carnaval
        pascoa - timedelta(days=47),  # Terça de Carnaval
        pascoa - timedelta(days=2),   # Sexta-Feira Santa
        pascoa + timedelta(days=60),  # Corpus Christi
    }
    fixos = {
        date(ano, 1, 1),    # Confraternização Universal
        date(ano, 4, 21),   # Tiradentes
        date(ano, 5, 1),    # Dia do Trabalho
        date(ano, 7, 9),    # Revolução Constitucionalista (SP)
        date(ano, 9, 7),    # Independência do Brasil
        date(ano, 10, 12),  # Nossa Senhora Aparecida
        date(ano, 11, 2),   # Finados
        date(ano, 11, 15),  # Proclamação da República
        date(ano, 11, 20),  # Consciência Negra
        date(ano, 12, 25),  # Natal
    }
    return fixos | moveis


def calcular_perfil_diurno_sp055(dt_sp: datetime) -> Tuple[float, Dict[str, float], float, str]:
    """
    Calcula o perfil realista da SP-055 para a data e hora exatas em São Paulo.

    Retorna:
        - fator_volume: multiplicador contínuo de fluxo (0.12 a 2.40)
        - proporcoes_sentido: divisão direcional exata {"Ubatuba": p1, "Maranduba": p2}
        - velocidade_media: velocidade média acoplada à densidade (km/h)
        - contexto_calendario: descrição do regime de tráfego aplicado
    """
    data_atual = dt_sp.date()
    dia_semana = dt_sp.weekday()  # 0=Seg .. 6=Dom
    hora = dt_sp.hour + (dt_sp.minute / 60.0) + (dt_sp.second / 3600.0)

    feriados = obter_feriados_sp(data_atual.year) | obter_feriados_sp(data_atual.year + 1)
    eh_feriado = data_atual in feriados
    vespera_feriado = (data_atual + timedelta(days=1)) in feriados
    pos_feriado = (data_atual - timedelta(days=1)) in feriados

    # 1. Sazonalidade mensal (Litoral Norte SP)
    fatores_mes = {
        1: 1.32,   # Janeiro (férias de verão)
        2: 1.24,   # Fevereiro (verão / Carnaval)
        3: 1.04,   # Março
        4: 0.96,   # Abril
        5: 0.88,   # Maio (baixa temporada)
        6: 0.90,   # Junho
        7: 1.20,   # Julho (férias escolares)
        8: 0.88,   # Agosto
        9: 0.94,   # Setembro
        10: 1.02,  # Outubro
        11: 1.08,  # Novembro
        12: 1.30,  # Dezembro (festas e verão)
    }
    fator_sazonal = fatores_mes.get(data_atual.month, 1.0)

    # 2. Curva horária contínua (soma de componentes suaves)
    piso_madrugada = 0.14
    pico_manha = 0.72 * _gaussiana(hora, centro=7.75, largura=1.45)
    platô_diurno = 0.78 * _gaussiana(hora, centro=12.80, largura=3.40)
    pico_tarde = 0.95 * _gaussiana(hora, centro=18.00, largura=1.55)
    noite_residual = 0.24 * _gaussiana(hora, centro=21.20, largura=1.40)

    fator_base = piso_madrugada + pico_manha + platô_diurno + pico_tarde + noite_residual
    prop_ubatuba = 0.50
    contexto = "Dia útil padrão"

    # 3. Dinâmica de fim de semana, feriados e emendas na SP-055
    if vespera_feriado or (dia_semana == 4 and not eh_feriado):
        contexto = "Véspera de feriado" if vespera_feriado else "Sexta-feira (descida litoral)"
        if hora >= 12.0:
            intensidade_descida = _gaussiana(hora, centro=18.5, largura=3.2)
            fator_base *= 1.0 + 0.52 * intensidade_descida
            prop_ubatuba = 0.50 + 0.24 * intensidade_descida
    elif eh_feriado and dia_semana in (0, 1, 2, 3, 4):
        contexto = "Feriado (fluxo turístico)"
        # Manhã com chegada à praia; fim de tarde com retorno se dia seguinte for útil
        if hora < 13.5:
            fator_base *= 1.22
            prop_ubatuba = 0.62
        elif not (data_atual + timedelta(days=1)) in feriados and dia_semana != 4:
            intensidade_retorno = _gaussiana(hora, centro=17.5, largura=2.8)
            fator_base *= 1.0 + 0.48 * intensidade_retorno
            prop_ubatuba = 0.50 - 0.24 * intensidade_retorno
        else:
            fator_base *= 1.15
            prop_ubatuba = 0.52
    elif dia_semana == 5:  # Sábado
        contexto = "Sábado litorâneo"
        if 7.5 <= hora <= 14.0:
            chegada_sabado = _gaussiana(hora, centro=10.5, largura=2.1)
            fator_base *= 1.0 + 0.40 * chegada_sabado
            prop_ubatuba = 0.50 + 0.18 * chegada_sabado
        elif 18.5 <= hora <= 22.5:
            # Movimento local noturno (restaurantes / centro)
            fator_base *= 1.14
            prop_ubatuba = 0.51
    elif dia_semana == 6 or (pos_feriado and dia_semana == 0):  # Domingo ou retorno de feriado
        contexto = "Domingo (retorno litoral)" if dia_semana == 6 else "Retorno pós-feriado"
        if 8.0 <= hora < 13.0:
            fator_base *= 1.08
            prop_ubatuba = 0.55
        elif hora >= 13.0:
            intensidade_retorno = _gaussiana(hora, centro=17.5, largura=2.9)
            fator_base *= 1.0 + 0.62 * intensidade_retorno
            prop_ubatuba = 0.50 - 0.27 * intensidade_retorno  # até ~0.23 Ubatuba / 0.77 Maranduba

    fator_final = max(0.12, fator_base * fator_sazonal)
    prop_ubatuba = round(min(0.82, max(0.18, prop_ubatuba)), 3)
    prop_maranduba = round(1.0 - prop_ubatuba, 3)

    # 4. Velocidade média acoplada à densidade da rodovia + pequeno ruído
    velocidade_livre = 82.0 if (hora < 5.5 or hora >= 22.5) else 76.0
    queda_fluxo = max(0.0, (fator_final - 0.45) * 18.5)
    velocidade = max(34.0, min(86.0, velocidade_livre - queda_fluxo + random.uniform(-2.2, 2.2)))

    return fator_final, {"Ubatuba": prop_ubatuba, "Maranduba": prop_maranduba}, round(velocidade, 1), contexto


def perfil_individual_camera(cam: Dict[str, Any]) -> Dict[str, float]:
    """
    Define características próprias de cada câmera para que pontos diferentes
    da SP-055 não tenham contagens idênticas.
    """
    nome = str(cam.get("nome", "")).lower()
    cam_id = str(cam.get("id", ""))

    if "36" in nome or "055" in str(cam.get("km", "")):
        # Trecho urbano / acesso praias: maior volume total e mais motos/carros locais
        return {"mult_vol": 1.18, "delta_motos": 0.03, "delta_pesados": -0.02}
    if "14" in nome or "211" in str(cam.get("km", "")):
        # Trecho rodoviário interurbano: fluxo mais constante e maior presença de caminhões/ônibus
        return {"mult_vol": 0.92, "delta_motos": -0.02, "delta_pesados": 0.03}

    # Perfil determinístico para qualquer outra câmera cadastrada no banco
    h = int(hashlib.md5(cam_id.encode("utf-8")).hexdigest()[:6], 16)
    mult = 0.85 + (h % 40) / 100.0  # 0.85 a 1.24
    return {"mult_vol": mult, "delta_motos": 0.0, "delta_pesados": 0.0}


def buscar_ultimo_total_camera(client, cam_id: str, agora_utc_dt: datetime) -> Optional[int]:
    """
    Busca o último total registrado para a câmera nos últimos 15 minutos
    para dar continuidade realista entre leituras de 5 em 5 minutos.
    """
    if not client:
        return None
    try:
        res = (
            client.table("contagens_minuto")
            .select("data_hora, carros, motos, onibus, caminhoes")
            .eq("camera_id", cam_id)
            .order("data_hora", desc=True)
            .limit(1)
            .execute()
        )
        if not res.data:
            return None
        ultimo = res.data[0]
        dt_str = str(ultimo["data_hora"]).replace("Z", "+00:00")
        dt_prev = datetime.fromisoformat(dt_str)
        if (agora_utc_dt - dt_prev).total_seconds() <= 900:  # até 15 min atrás
            return (
                int(ultimo.get("carros", 0))
                + int(ultimo.get("motos", 0))
                + int(ultimo.get("onibus", 0))
                + int(ultimo.get("caminhoes", 0))
            )
    except Exception:
        pass
    return None


def gerar_contagens_veiculos(
    fator_volume: float,
    dt_sp: datetime,
    perfil_cam: Dict[str, float],
    ultimo_total: Optional[int] = None,
) -> Dict[str, int]:
    """
    Gera contagens por minuto realistas combinando curva horária,
    composição de frota por período (comercial vs. lazer/madrugada)
    e inércia temporal.
    """
    # Volume base médio de 16 veículos/min em fluxo diurno padrão na SP-055
    alvo_teorico = 16.0 * fator_volume * perfil_cam["mult_vol"]

    if ultimo_total is not None and ultimo_total > 0:
        # 65% alvo atual + 35% inércia da leitura de 5 minutos atrás
        media_esperada = (0.65 * alvo_teorico) + (0.35 * ultimo_total)
    else:
        media_esperada = alvo_teorico

    # Dispersão estatística proporcional à raiz da média (comportamento de contagem viária)
    desvio = max(1.0, math.sqrt(media_esperada) * 0.85)
    total_veiculos = max(1, int(round(random.gauss(media_esperada, desvio))))

    hora = dt_sp.hour + dt_sp.minute / 60.0
    fim_de_semana = dt_sp.weekday() in (5, 6)

    # Composição de frota varia conforme horário comercial vs. fim de semana/madrugada
    if 0 <= hora < 5:
        p_motos = 0.06
        p_caminhoes = 0.16
        p_onibus = 0.04
    elif fim_de_semana:
        p_motos = 0.13
        p_caminhoes = 0.04
        p_onibus = 0.04
    elif 7 <= hora <= 18:
        p_motos = 0.14
        p_caminhoes = 0.13
        p_onibus = 0.05
    else:
        p_motos = 0.11
        p_caminhoes = 0.08
        p_onibus = 0.04

    p_motos = max(0.02, p_motos + perfil_cam["delta_motos"] + random.uniform(-0.02, 0.02))
    p_caminhoes = max(0.01, p_caminhoes + perfil_cam["delta_pesados"] + random.uniform(-0.02, 0.02))
    p_onibus = max(0.01, p_onibus + random.uniform(-0.01, 0.015))

    n_motos = int(round(total_veiculos * p_motos))
    n_caminhoes = int(round(total_veiculos * p_caminhoes))
    n_onibus = int(round(total_veiculos * p_onibus))

    # Ajusta caso a soma das minorias ultrapasse o total em fluxos muito baixos
    while (n_motos + n_caminhoes + n_onibus) > max(0, total_veiculos - 1) and total_veiculos > 1:
        if n_onibus > 0:
            n_onibus -= 1
        elif n_caminhoes > 0:
            n_caminhoes -= 1
        elif n_motos > 0:
            n_motos -= 1

    n_carros = max(0, total_veiculos - (n_motos + n_onibus + n_caminhoes))

    return {
        "carros": n_carros,
        "motos": n_motos,
        "onibus": n_onibus,
        "caminhoes": n_caminhoes,
    }


def dividir_por_sentidos_exato(
    contagem: Dict[str, int], proporcoes: Dict[str, float]
) -> Dict[str, Dict[str, int]]:
    """
    Divide cada categoria entre os sentidos garantindo que a soma
    dos sentidos seja exatamente igual ao total registrado em contagens_minuto.
    """
    sentidos = list(proporcoes.keys())
    s1, s2 = sentidos[0], sentidos[1]
    p1 = proporcoes[s1]

    resultado = {s1: {}, s2: {}}
    for cat in ("carros", "motos", "onibus", "caminhoes"):
        total_cat = contagem[cat]
        # Pequena variação natural na divisão direcional para contagens maiores
        p_efetivo = p1 if total_cat < 4 else min(0.90, max(0.10, p1 + random.uniform(-0.04, 0.04)))
        qtd_s1 = int(round(total_cat * p_efetivo))
        qtd_s1 = max(0, min(total_cat, qtd_s1))
        qtd_s2 = total_cat - qtd_s1

        resultado[s1][cat] = qtd_s1
        resultado[s2][cat] = qtd_s2

    return resultado


def sincronizar_storage(client, dry_run: bool = False) -> str:
    """
    Garante a existência do bucket 'camera-captures' e realiza upload
    de imagens reais de amostra.
    """
    if dry_run or not client:
        return "[DRY-RUN] Upload simulado de latest.jpg e camera_36.jpg para bucket 'camera-captures'"

    try:
        buckets = client.storage.list_buckets()
        bucket_names = [b.name if hasattr(b, "name") else b.get("name") for b in buckets]
        if "camera-captures" not in bucket_names:
            try:
                client.storage.create_bucket("camera-captures", options={"public": True})
                print("[Storage] Bucket 'camera-captures' criado com sucesso.")
            except Exception as e:
                print(f"[Storage] Nota ao criar bucket: {e}")

        for f_name in ["latest.jpg", "camera_36.jpg"]:
            f_path = SAMPLE_DIR / f_name
            if f_path.exists():
                with open(f_path, "rb") as f:
                    file_bytes = f.read()
                try:
                    client.storage.from_("camera-captures").upload(
                        path=f_name,
                        file=file_bytes,
                        file_options={"content-type": "image/jpeg", "upsert": "true"},
                    )
                    print(f"[Storage] Upload de {f_name} realizado com sucesso.")
                except Exception as ue:
                    print(f"[Storage] Nota no upload de {f_name}: {ue}")

        return "Upload para Supabase Storage finalizado."
    except Exception as e:
        return f"[Storage] Erro ao sincronizar storage: {e}"


def main():
    parser = argparse.ArgumentParser(description="Pipeline de Alimentação Contínua RoadVision (CI/CD)")
    parser.add_argument("--dry-run", action="store_true", help="Executa simulação sem gravar no banco")
    args = parser.parse_args()

    agora_sp = datetime.now(TZ_SP)
    agora_utc_dt = agora_sp.astimezone(timezone.utc)
    agora_utc = agora_utc_dt.isoformat()

    print("=== RoadVision Continuous Feed Pipeline (5 min) ===")
    print(f"Data/Hora Local: {agora_sp.strftime('%d/%m/%Y %H:%M:%S')} ({TZ_SP})")
    print(f"Data/Hora UTC:   {agora_utc}")
    print(f"Modo de Execução: {'[DRY-RUN - Apenas Simulação]' if args.dry_run else '[LIVE - Escrita em Supabase]'}")

    fator_vol, proporcoes_sentido, vel_media, contexto = calcular_perfil_diurno_sp055(agora_sp)
    print(f"Contexto SP-055: {contexto}")
    print(f"Perfil Diurno:   Fator={fator_vol:.2f} | Velocidade={vel_media} km/h | Sentidos={proporcoes_sentido}")

    client = get_supabase()
    cameras_db = []
    if client:
        try:
            res = client.table("cameras").select("id, nome, km, ativa").execute()
            cameras_db = [c for c in (res.data or []) if c.get("ativa", True)]
        except Exception as e:
            print(f"[Aviso] Falha ao consultar câmeras do Supabase: {e}")

    if not cameras_db:
        cameras_db = [
            {"id": "aa708460-ea62-48f2-b924-e5e058e3ed89", "nome": "DER SP - Camera 36", "km": "055+000"},
            {"id": "5144fc7b-a590-4de3-b338-700bda1ef368", "nome": "DER SP - Camera 14", "km": "211+000"},
        ]

    print(f"Câmeras identificadas para alimentação: {len(cameras_db)}")

    payload_minuto = []
    payload_sentido = []

    for cam in cameras_db:
        cam_id = cam["id"]
        cam_nome = cam.get("nome", f"Camera {cam_id}")
        perfil_cam = perfil_individual_camera(cam)
        ultimo_total = None if args.dry_run else buscar_ultimo_total_camera(client, cam_id, agora_utc_dt)

        contagem = gerar_contagens_veiculos(fator_vol, agora_sp, perfil_cam, ultimo_total)
        por_sentido = dividir_por_sentidos_exato(contagem, proporcoes_sentido)

        payload_minuto.append({
            "camera_id": cam_id,
            "data_hora": agora_utc,
            "carros": contagem["carros"],
            "motos": contagem["motos"],
            "onibus": contagem["onibus"],
            "caminhoes": contagem["caminhoes"],
        })

        for sentido, vals in por_sentido.items():
            payload_sentido.append({
                "camera_id": cam_id,
                "data_hora": agora_utc,
                "sentido": sentido,
                "carros": vals["carros"],
                "motos": vals["motos"],
                "onibus": vals["onibus"],
                "caminhoes": vals["caminhoes"],
            })

        total_cam = sum(contagem.values())
        print(
            f"  -> {cam_nome}: Total={total_cam} veíc "
            f"(Carros={contagem['carros']}, Motos={contagem['motos']}, "
            f"Ônibus={contagem['onibus']}, Caminhões={contagem['caminhoes']}) "
            f"| Ubatuba={sum(por_sentido['Ubatuba'].values())}, Maranduba={sum(por_sentido['Maranduba'].values())}"
        )

    if args.dry_run:
        print("\n[DRY-RUN] Nenhuma gravação executada no Supabase.")
        print(f"[DRY-RUN] Registros contagens_minuto: {len(payload_minuto)}")
        print(f"[DRY-RUN] Registros contagens_por_sentido: {len(payload_sentido)}")
        print(f"[DRY-RUN] {sincronizar_storage(client, dry_run=True)}")
    else:
        if not client:
            print("[ERRO] Supabase não está configurado. Abortando gravação.")
            sys.exit(1)

        houve_erro = False
        try:
            client.table("contagens_minuto").insert(payload_minuto).execute()
            print(f"[Banco] {len(payload_minuto)} registros inseridos em contagens_minuto.")
        except Exception as e:
            print(f"[ERRO] Falha ao inserir em contagens_minuto: {e}")
            houve_erro = True

        try:
            client.table("contagens_por_sentido").insert(payload_sentido).execute()
            print(f"[Banco] {len(payload_sentido)} registros inseridos em contagens_por_sentido.")
        except Exception as e:
            print(f"[ERRO] Falha ao inserir em contagens_por_sentido: {e}")
            houve_erro = True

        storage_res = sincronizar_storage(client, dry_run=False)
        print(f"[Storage] {storage_res}")

        if houve_erro:
            sys.exit(1)

    print("=== Pipeline executado com sucesso. ===")


if __name__ == "__main__":
    main()
