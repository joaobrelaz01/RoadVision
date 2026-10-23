import json
import time
from collections import Counter
from pathlib import Path

import cv2

from roadvision.detection.contagem_linha_virtual import (
    LinhaVirtualContagem,
    SENTIDO_1,
    SENTIDO_2,
)
from roadvision.detection.detector_yolo import YOLODetector
from roadvision.tracking import VehicleTracker


ROOT = Path(__file__).resolve().parents[3]
CAMERAS_PATH = ROOT / "configs" / "cameras" / "cameras.json"
OUTPUT_PATH = ROOT / "data" / "resultados" / "counting" / "contagem_automatica.json"

CAMERA_ID = 36
PONTO_INICIAL = (120, 350)
PONTO_FINAL = (430, 125)


def carregar_camera():
    with CAMERAS_PATH.open("r", encoding="utf-8-sig") as arquivo:
        cameras = json.load(arquivo)["cameras"]

    camera = next(
        (item for item in cameras if item["id"] == CAMERA_ID),
        None,
    )
    if camera is None:
        raise RuntimeError(f"Câmera {CAMERA_ID} não encontrada.")

    return camera


def main():
    camera = carregar_camera()

    print(f"Câmera: {camera['nome']}")
    print("Carregando modelo YOLO e rastreador...")

    detector = YOLODetector()
    tracker = VehicleTracker(detector.model)
    linha = LinhaVirtualContagem(PONTO_INICIAL, PONTO_FINAL)

    captura = cv2.VideoCapture(camera["stream_url"], cv2.CAP_FFMPEG)
    if not captura.isOpened():
        captura.release()
        raise RuntimeError("Não foi possível abrir o stream da câmera.")

    contagens = Counter({
        SENTIDO_1: 0,
        SENTIDO_2: 0,
    })
    inicio = time.monotonic()

    try:
        while True:
            sucesso, frame = captura.read()
            if not sucesso or frame is None:
                print("Falha ao ler o frame.")
                break

            resultado = tracker.track(frame)

            for track_id in tracker.get_active_ids():
                trajetoria = tracker.get_trajectory(track_id)
                if len(trajetoria) < 2:
                    continue

                sentido = linha.verificar_cruzamento(
                    track_id,
                    trajetoria[-2],
                    trajetoria[-1],
                )

                if sentido in contagens:
                    contagens[sentido] += 1
                    print(f"ID {track_id} cruzou: {sentido}")

            imagem = resultado.plot()
            cv2.line(
                imagem, PONTO_INICIAL, PONTO_FINAL,
                (0, 255, 255), 2,
            )

            cv2.putText(
                imagem,
                f"Negativo -> positivo: {contagens[SENTIDO_1]}",
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (0, 255, 0), 2,
            )
            cv2.putText(
                imagem,
                f"Positivo -> negativo: {contagens[SENTIDO_2]}",
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (0, 255, 0), 2,
            )
            cv2.imshow("RoadVision - Validacao da contagem", imagem)

            tecla = cv2.waitKey(1) & 0xFF
            if tecla in (27, ord("q")):
                break

    finally:
        captura.release()
        cv2.destroyAllWindows()

    duracao = round(time.monotonic() - inicio, 2)

    relatorio = {
        SENTIDO_1: contagens[SENTIDO_1],
        SENTIDO_2: contagens[SENTIDO_2],
        "camera_id": CAMERA_ID,
        "camera_nome": camera["nome"],
        "duracao_segundos": duracao,
        "total_automatico": sum(contagens.values()),
        "observacao": (
            "Contagem obtida durante uma captura ao vivo. "
            "Para validar a precisao, compare com a contagem manual "
            "do mesmo intervalo."
        ),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")

    print("\n--- Resultado da contagem ---")
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    print(f"Arquivo salvo em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
