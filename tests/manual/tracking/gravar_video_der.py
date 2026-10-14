
import argparse
import time
from pathlib import Path

import cv2


ROOT_DIR = Path(__file__).resolve().parents[3]
VIDEO_DIR = ROOT_DIR / "data" / "videos"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=14)
    parser.add_argument("--duracao", type=int, default=60)
    args = parser.parse_args()

    if args.duracao < 1:
        parser.error("--duracao deve ser maior que zero.")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    url = (
        "http://200.144.30.103:8084/hls/"
        f"cam_{args.camera}/stream.m3u8"
    )

    print(f"Abrindo camera DER/SP {args.camera}...")
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        raise RuntimeError("Nao foi possivel abrir a transmissao.")

    writer = None
    frames = 0
    inicio = time.perf_counter()
    caminho = VIDEO_DIR / f"der_cam_{args.camera}.mp4"

    try:
        while time.perf_counter() - inicio < args.duracao:
            sucesso, frame = cap.read()

            if not sucesso:
                print("Falha na leitura do stream.")
                break

            if writer is None:
                fps = cap.get(cv2.CAP_PROP_FPS)
                if not 1 <= fps <= 60:
                    fps = 20.0

                altura, largura = frame.shape[:2]
                codec = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter(
                    str(caminho),
                    codec,
                    fps,
                    (largura, altura),
                )

                if not writer.isOpened():
                    raise RuntimeError("Nao foi possivel criar o arquivo.")

            writer.write(frame)
            frames += 1

    finally:
        cap.release()

        if writer is not None:
            writer.release()

    print(f"Frames gravados: {frames}")
    print(f"Arquivo: {caminho}")

    if frames == 0:
        caminho.unlink(missing_ok=True)
        raise RuntimeError("Nenhum frame foi gravado.")

    print("Confira o video antes de usa-lo no teste.")


if __name__ == "__main__":
    main()
