import cv2
from pathlib import Path


CAMERA_URL = "http://200.144.30.103:8084/hls/cam_36/stream.m3u8"
FRAMES_DIR = Path("tests/frames")


def testar_captura_camera_real():
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    captura = cv2.VideoCapture(CAMERA_URL, cv2.CAP_FFMPEG)

    if not captura.isOpened():
        raise RuntimeError("Não foi possível abrir o stream da câmera.")

    print("Stream da câmera aberto com sucesso.")

    for numero_frame in range(5):
        sucesso, frame = captura.read()

        if not sucesso:
            raise RuntimeError(
                f"Não foi possível obter o frame {numero_frame}."
            )

        caminho_frame = FRAMES_DIR / f"frame_{numero_frame}.jpg"

        cv2.imwrite(str(caminho_frame), frame)

        print(
            f"Frame {numero_frame} obtido: "
            f"{frame.shape[1]}x{frame.shape[0]}"
        )

    captura.release()

    print("Captura finalizada com sucesso.")


if __name__ == "__main__":
    testar_captura_camera_real()