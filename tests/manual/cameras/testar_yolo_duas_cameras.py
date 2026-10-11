
import csv
import json
import time
from pathlib import Path

import cv2
import psutil

from roadvision.detection.detector_yolo import YOLODetector


RAIZ = Path(__file__).resolve().parents[3]
CONFIG = RAIZ / "configs" / "cameras" / "cameras.json"
RELATORIO = (
    RAIZ / "tests" / "manual" / "cameras"
    / "resultado_yolo_duas_cameras.csv"
)

IDS_CAMERAS = [11, 37]
DURACAO_SEGUNDOS = 60
TIMEOUT_ABERTURA_MS = 8000
TIMEOUT_LEITURA_MS = 5000
CLASSES_VEICULOS = [2, 3, 5, 7]


def carregar_cameras():
    with CONFIG.open("r", encoding="utf-8-sig") as arquivo:
        dados = json.load(arquivo)

    cameras = {
        int(camera["id"]): camera
        for camera in dados["cameras"]
    }

    ausentes = [id_camera for id_camera in IDS_CAMERAS
                if id_camera not in cameras]

    if ausentes:
        raise ValueError(f"Câmeras não encontradas: {ausentes}")

    return [cameras[id_camera] for id_camera in IDS_CAMERAS]


def main():
    cameras = carregar_cameras()
    capturas = {}
    resultados = {}

    print("RoadVision - Benchmark YOLO")
    print("Câmeras:", IDS_CAMERAS)
    print(f"Duração: {DURACAO_SEGUNDOS} segundos")
    print("Carregando o modelo uma única vez...")

    detector = YOLODetector()
    modelo = detector.model

    processo = psutil.Process()
    processo.cpu_percent()
    memoria_inicial_mb = (
        processo.memory_info().rss / (1024 * 1024)
    )

    try:
        # Abre as duas câmeras antes de iniciar a medição.
        for camera in cameras:
            camera_id = int(camera["id"])
            print(
                f"Abrindo ID {camera_id}: "
                f"{camera['nome']}"
            )

            captura = cv2.VideoCapture(
                camera["stream_url"],
                cv2.CAP_FFMPEG,
                [
                    cv2.CAP_PROP_OPEN_TIMEOUT_MSEC,
                    TIMEOUT_ABERTURA_MS,
                    cv2.CAP_PROP_READ_TIMEOUT_MSEC,
                    TIMEOUT_LEITURA_MS,
                ],
            )

            if not captura.isOpened():
                captura.release()
                print(f"AVISO: câmera {camera_id} indisponível.")
                continue

            capturas[camera_id] = captura
            resultados[camera_id] = {
                "camera_id": camera_id,
                "nome": camera["nome"],
                "frames_validos": 0,
                "falhas_captura": 0,
                "infracoes_yolo": 0,
                "deteccoes": 0,
                "tempo_inferencia_ms": 0.0,
                "infracoes_erro": 0,
            }

        if not capturas:
            print("Nenhuma câmera foi aberta.")
            return

        inicio = time.monotonic()
        prazo = inicio + DURACAO_SEGUNDOS

        print("\nTeste iniciado. Aguarde...")
        while time.monotonic() < prazo:
            for camera_id, captura in list(capturas.items()):
                if time.monotonic() >= prazo:
                    break

                dados = resultados[camera_id]
                sucesso, frame = captura.read()

                if not sucesso or frame is None:
                    dados["falhas_captura"] += 1
                    continue

                dados["frames_validos"] += 1

                # Detecção, sem rastreamento persistente.
                # O mesmo modelo é usado sequencialmente.
                inicio_inferencia = time.perf_counter()

                try:
                    previsoes = modelo.predict(
                        frame,
                        classes=CLASSES_VEICULOS,
                        imgsz=640,
                        verbose=False,
                    )

                    dados["tempo_inferencia_ms"] += (
                        time.perf_counter() - inicio_inferencia
                    ) * 1000

                    dados["infracoes_yolo"] += 1
                    caixas = previsoes[0].boxes

                    if caixas is not None:
                        dados["deteccoes"] += len(caixas)

                except Exception as erro:
                    dados["infracoes_erro"] += 1
                    print(
                        f"Erro no YOLO da câmera {camera_id}: "
                        f"{erro}"
                    )

        duracao_real = time.monotonic() - inicio
        cpu_percent = processo.cpu_percent()
        memoria_final_mb = (
            processo.memory_info().rss / (1024 * 1024)
        )

    finally:
        for captura in capturas.values():
            captura.release()

    colunas = [
        "camera_id",
        "nome",
        "frames_validos",
        "falhas_captura",
        "infracoes_yolo",
        "deteccoes",
        "fps_inferencia",
        "media_inferencia_ms",
        "infracoes_erro",
    ]

    linhas = []

    print("\n--- RESULTADOS POR CÂMERA ---")

    for dados in resultados.values():
        quantidade = dados["infracoes_yolo"]
        tempo_ms = dados["tempo_inferencia_ms"]

        dados["fps_inferencia"] = round(
            quantidade / duracao_real, 2
        )
        dados["media_inferencia_ms"] = round(
            tempo_ms / quantidade, 2
        ) if quantidade else 0

        linha = {chave: dados[chave] for chave in colunas}
        linhas.append(linha)

        print(
            f"ID {dados['camera_id']} | "
            f"Frames: {dados['frames_validos']} | "
            f"Falhas: {dados['falhas_captura']} | "
            f"FPS de inferência: {dados['fps_inferencia']} | "
            f"Média YOLO: {dados['media_inferencia_ms']} ms"
        )

    RELATORIO.parent.mkdir(parents=True, exist_ok=True)

    with RELATORIO.open(
        "w", newline="", encoding="utf-8-sig"
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=colunas
        )
        escritor.writeheader()
        escritor.writerows(linhas)

    print("\n--- RECURSOS ---")
    print(f"Duração real: {duracao_real:.1f} s")
    print(f"CPU do processo (%): {cpu_percent:.1f}")
    print(f"Memória inicial: {memoria_inicial_mb:.1f} MB")
    print(f"Memória final: {memoria_final_mb:.1f} MB")
    print(f"Relatório: {RELATORIO}")


if __name__ == "__main__":
    main()
