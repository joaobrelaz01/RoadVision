import json
from pathlib import Path

import cv2


ROOT = Path(__file__).resolve().parents[3]
CAMERAS_PATH = ROOT / "configs" / "cameras" / "cameras.json"
OUTPUT_DIR = ROOT / "tests" / "manual" / "counting" / "frames"


def main():
    with open(CAMERAS_PATH, "r", encoding="utf-8") as arquivo:
        cameras = json.load(arquivo)["cameras"]

    camera = next(
        (item for item in cameras if item["id"] == 36),
        None,
    )

    if camera is None:
        raise RuntimeError("Câmera 36 não encontrada na configuração.")

    print(f"Câmera: {camera['nome']}")
    print(f"Stream: {camera['stream_url']}")
    print("Conectando ao stream...")

    captura = cv2.VideoCapture(
        camera["stream_url"],
        cv2.CAP_FFMPEG,
    )

    try:
        if not captura.isOpened():
            raise RuntimeError("Não foi possível abrir a câmera 36.")

        sucesso, frame = captura.read()

        if not sucesso or frame is None:
            raise RuntimeError("Não foi possível obter um frame.")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        destino = OUTPUT_DIR / "camera_36.jpg"

        if not cv2.imwrite(str(destino), frame):
            raise RuntimeError("Não foi possível salvar a imagem.")

        altura, largura = frame.shape[:2]

        print(f"Frame salvo em: {destino}")
        print(f"Resolução capturada: {largura}x{altura}")

    finally:
        captura.release()


if __name__ == "__main__":
    main()