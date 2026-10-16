import json
from pathlib import Path

import cv2

from roadvision.detection.contagem_linha_virtual import LinhaVirtualContagem
from roadvision.detection.detector_yolo import YOLODetector
from roadvision.tracking import VehicleTracker


ROOT = Path(__file__).resolve().parents[3]
CAMERAS_PATH = ROOT / "configs" / "cameras" / "cameras.json"

# Coordenadas iniciais: validar visualmente antes de considerar definitivas.
PONTO_INICIAL = (120, 350)
PONTO_FINAL = (430, 125)

CAMERA_ID = 36


def carregar_camera():
    with open(CAMERAS_PATH, "r", encoding="utf-8") as arquivo:
        cameras = json.load(arquivo)["cameras"]

    camera = next(
        (item for item in cameras if item["id"] == CAMERA_ID),
        None,
    )

    if camera is None:
        raise RuntimeError(f"Câmera {CAMERA_ID} não encontrada.")

    return camera


def desenhar_linha(frame):
    cv2.line(
        frame,
        PONTO_INICIAL,
        PONTO_FINAL,
        (0, 255, 255),
        2,
    )
    cv2.circle(frame, PONTO_INICIAL, 5, (0, 255, 0), -1)
    cv2.circle(frame, PONTO_FINAL, 5, (0, 0, 255), -1)


def main():
    camera = carregar_camera()

    print(f"Câmera: {camera['nome']}")
    print(f"Stream: {camera['stream_url']}")
    print("Carregando YOLO e ByteTrack...")

    detector = YOLODetector()
    tracker = VehicleTracker(detector.model)

    contador = LinhaVirtualContagem(
        PONTO_INICIAL,
        PONTO_FINAL,
    )

    captura = cv2.VideoCapture(
        camera["stream_url"],
        cv2.CAP_FFMPEG,
    )

    if not captura.isOpened():
        captura.release()
        raise RuntimeError("Não foi possível abrir o stream.")

    ultimos_cruzamentos = []

    try:
        while True:
            sucesso, frame = captura.read()

            if not sucesso or frame is None:
                print("Falha na leitura do frame.")
                break

            resultado = tracker.track(frame)
            ultimos_cruzamentos = []

            for track_id in tracker.get_active_ids():
                trajetoria = tracker.get_trajectory(track_id)

                if len(trajetoria) < 2:
                    continue

                ponto_anterior = trajetoria[-2]
                ponto_atual = trajetoria[-1]

                sentido = contador.verificar_cruzamento(
                    track_id,
                    ponto_anterior,
                    ponto_atual,
                )

                if sentido:
                    ultimos_cruzamentos.append(
                        (track_id, sentido)
                    )
                    print(
                        f"Veículo ID {track_id} cruzou a linha: "
                        f"{sentido}"
                    )

            # Mantém as caixas e IDs gerados pelo resultado do rastreador.
            imagem = resultado.plot()
            desenhar_linha(imagem)

            cv2.putText(
                imagem,
                f"Total contado: {contador.total_contado()}",
                (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            y_texto = 95
            for track_id, sentido in ultimos_cruzamentos:
                texto = f"ID {track_id}: {sentido}"
                cv2.putText(
                    imagem,
                    texto,
                    (20, y_texto),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (0, 255, 255),
                    1,
                )
                y_texto += 22

            cv2.imshow("RoadVision - Linha virtual + ByteTrack", imagem)

            tecla = cv2.waitKey(1) & 0xFF
            if tecla == 27 or tecla == ord("q"):
                break

    finally:
        captura.release()
        cv2.destroyAllWindows()

    print("\n--- Resultado do teste ---")
    print(f"Câmera: {camera['nome']}")
    print(f"IDs únicos rastreados: {tracker.get_unique_count()}")
    print(f"Veículos contados: {contador.total_contado()}")


if __name__ == "__main__":
    main()