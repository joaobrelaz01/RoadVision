from pathlib import Path

import cv2


ROOT = Path(__file__).resolve().parents[3]
FRAME_PATH = ROOT / "tests" / "manual" / "counting" / "frames" / "camera_36.jpg"
OUTPUT_PATH = ROOT / "tests" / "manual" / "counting" / "frames" / "camera_36_linha.jpg"

# Coordenadas iniciais para validação visual.
PONTO_INICIAL = (165, 315)
PONTO_FINAL = (365, 165)


def main():
    if not FRAME_PATH.exists():
        raise FileNotFoundError(
            f"Frame não encontrado: {FRAME_PATH}"
        )

    frame = cv2.imread(str(FRAME_PATH))

    if frame is None:
        raise RuntimeError("Não foi possível carregar o frame.")

    # Desenha a linha virtual.
    cv2.line(
        frame,
        PONTO_INICIAL,
        PONTO_FINAL,
        (0, 255, 255),
        3,
    )

    cv2.circle(frame, PONTO_INICIAL, 6, (0, 255, 0), -1)
    cv2.circle(frame, PONTO_FINAL, 6, (0, 0, 255), -1)

    cv2.putText(
        frame,
        "LINHA VIRTUAL - TESTE",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2,
    )

    if not cv2.imwrite(str(OUTPUT_PATH), frame):
        raise RuntimeError("Não foi possível salvar a imagem de teste.")

    print(f"Imagem original: {FRAME_PATH}")
    print(f"Imagem com linha: {OUTPUT_PATH}")
    print(f"Ponto inicial: {PONTO_INICIAL}")
    print(f"Ponto final: {PONTO_FINAL}")

    cv2.imshow("RoadVision - Linha Virtual", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()