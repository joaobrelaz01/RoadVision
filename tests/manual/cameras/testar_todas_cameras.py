
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import cv2


# Configurações do teste
ARQUIVO_CONFIG = Path("configs/cameras/cameras.json")
ARQUIVO_RELATORIO = Path("tests/manual/cameras/resultado_cameras.csv")

DURACAO_TESTE = 30
TIMEOUT_ABERTURA_MS = 8000
TIMEOUT_LEITURA_MS = 5000
MAX_WORKERS = 10

# Câmera confirmada em manutenção.
CAMERAS_EM_MANUTENCAO = {10}


def primeiro_valor(dados, chaves):
    """Retorna o primeiro campo existente e preenchido."""
    for chave in chaves:
        valor = dados.get(chave)
        if valor is not None and valor != "":
            return valor
    return None


def carregar_cameras():
    with ARQUIVO_CONFIG.open("r", encoding="utf-8-sig") as arquivo:
        dados = json.load(arquivo)

    cameras = dados["cameras"]

    if not isinstance(cameras, list):
        raise ValueError(
            "A chave 'cameras' precisa conter uma lista no JSON."
        )

    return cameras


def testar_camera(camera):
    camera_id = primeiro_valor(
        camera, ["id", "camera_id", "cameraId"]
    )

    nome = primeiro_valor(
        camera, ["nome", "name", "localizacao", "local"]
    ) or f"Câmera {camera_id}"

    if camera_id is None:
        return {
            "camera_id": "desconhecido",
            "nome": nome,
            "status": "ERRO_CONFIGURACAO",
            "frames": 0,
            "tempo_segundos": 0,
            "fps_medio": 0,
            "falhas_leitura": 0,
            "detalhe": "ID não encontrado no JSON",
        }

    if str(camera_id).strip() in {
        str(item) for item in CAMERAS_EM_MANUTENCAO
    }:
        return {
            "camera_id": camera_id,
            "nome": nome,
            "status": "MANUTENCAO",
            "frames": 0,
            "tempo_segundos": 0,
            "fps_medio": 0,
            "falhas_leitura": 0,
            "detalhe": "Ignorada durante a manutenção",
        }

    url = primeiro_valor(
        camera,
        ["stream_url", "url", "hls_url", "url_hls", "stream"]
    )

    if not url:
        return {
            "camera_id": camera_id,
            "nome": nome,
            "status": "ERRO_CONFIGURACAO",
            "frames": 0,
            "tempo_segundos": 0,
            "fps_medio": 0,
            "falhas_leitura": 0,
            "detalhe": "URL do vídeo não encontrada no JSON",
        }

    inicio = time.monotonic()
    captura = None
    frames = 0
    falhas = 0
    status = "ERRO_ABERTURA"
    detalhe = ""

    try:
        parametros = [
            cv2.CAP_PROP_OPEN_TIMEOUT_MSEC,
            TIMEOUT_ABERTURA_MS,
            cv2.CAP_PROP_READ_TIMEOUT_MSEC,
            TIMEOUT_LEITURA_MS,
        ]

        captura = cv2.VideoCapture(
            url, cv2.CAP_FFMPEG, parametros
        )

        if not captura.isOpened():
            detalhe = "Não foi possível abrir o stream"
        else:
            status = "OK"
            prazo = time.monotonic() + DURACAO_TESTE

            while time.monotonic() < prazo:
                sucesso, frame = captura.read()

                if sucesso and frame is not None:
                    frames += 1
                else:
                    falhas += 1
                    status = "LEITURA_COM_FALHAS"

            if frames == 0:
                status = "SEM_FRAMES"
                detalhe = "Conexão aberta, mas nenhum frame válido"
            elif falhas == 0:
                status = "OK"
            else:
                detalhe = "Ocorreram falhas durante a leitura"

    except Exception as erro:
        status = "ERRO"
        detalhe = str(erro)

    finally:
        if captura is not None:
            captura.release()

    tempo = time.monotonic() - inicio

    return {
        "camera_id": camera_id,
        "nome": nome,
        "status": status,
        "frames": frames,
        "tempo_segundos": round(tempo, 2),
        "fps_medio": round(frames / tempo, 2) if tempo > 0 else 0,
        "falhas_leitura": falhas,
        "detalhe": detalhe,
    }


def main():
    cameras = carregar_cameras()

    disponiveis = [
        camera for camera in cameras
        if str(primeiro_valor(
            camera, ["id", "camera_id", "cameraId"]
        )).strip() not in {
            str(item) for item in CAMERAS_EM_MANUTENCAO
        }
    ]

    ignoradas = len(cameras) - len(disponiveis)

    print(f"Câmeras cadastradas: {len(cameras)}")
    print(f"Câmeras que serão testadas: {len(disponiveis)}")
    print(f"Câmeras ignoradas por manutenção: {ignoradas}")
    print(f"Duração por câmera: {DURACAO_TESTE} segundos")
    print("\nIniciando testes simultâneos...\n")

    resultados = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        tarefas = {
            executor.submit(testar_camera, camera): camera
            for camera in disponiveis
        }

        for tarefa in as_completed(tarefas):
            resultado = tarefa.result()
            resultados.append(resultado)

            print(
                f"ID {resultado['camera_id']} | "
                f"{resultado['nome']} | "
                f"{resultado['status']} | "
                f"Frames: {resultado['frames']} | "
                f"FPS médio: {resultado['fps_medio']}"
            )

    # Registra a câmera em manutenção no relatório.
    for camera in cameras:
        camera_id = primeiro_valor(
            camera, ["id", "camera_id", "cameraId"]
        )
        if str(camera_id).strip() in {
            str(item) for item in CAMERAS_EM_MANUTENCAO
        }:
            resultados.append(testar_camera(camera))

    ARQUIVO_RELATORIO.parent.mkdir(
        parents=True, exist_ok=True
    )

    colunas = [
        "camera_id",
        "nome",
        "status",
        "frames",
        "tempo_segundos",
        "fps_medio",
        "falhas_leitura",
        "detalhe",
    ]

    with ARQUIVO_RELATORIO.open(
        "w", newline="", encoding="utf-8-sig"
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=colunas
        )
        escritor.writeheader()
        escritor.writerows(resultados)

    sucessos = sum(
        resultado["status"] == "OK"
        for resultado in resultados
    )

    print("\n--- RESUMO ---")
    print(f"Total cadastrado: {len(cameras)}")
    print(f"Câmeras com leitura sem falhas: {sucessos}")
    print(f"Relatório salvo em: {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    main()
