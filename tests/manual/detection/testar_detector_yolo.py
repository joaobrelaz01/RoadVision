
import cv2
import time

from roadvision.detection.detector_yolo import YOLODetector


STREAM_URL = "http://200.144.30.103:8084/hls/cam_14/stream.m3u8"


def main():
    print("Carregando detector...")
    detector = YOLODetector()

    print("Abrindo camera...")
    cap = cv2.VideoCapture(STREAM_URL)

    if not cap.isOpened():
        print("Nao foi possivel abrir a camera.")
        raise SystemExit(1)

    print("Camera aberta com sucesso!")

    total_frames = 0
    tempo_total = 0.0

    try:
        while True:
            sucesso, frame = cap.read()

            if not sucesso:
                print("Falha ao capturar frame.")
                break

            frame = cv2.resize(frame, (640, 360))

            inicio = time.perf_counter()
            resultado = detector.detect(frame)
            fim = time.perf_counter()

            tempo_total += fim - inicio
            total_frames += 1

            if total_frames % 30 == 0:
                print(f"Frames processados: {total_frames}")

            frame_analisado = resultado.plot()
            cv2.imshow("RoadVision - Detector YOLO", frame_analisado)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    if total_frames > 0:
        tempo_medio = tempo_total / total_frames
        fps = 1 / tempo_medio if tempo_medio > 0 else 0

        print("\n===== DESEMPENHO DO YOLO =====")
        print(f"Frames processados: {total_frames}")
        print(f"Tempo medio por frame: {tempo_medio * 1000:.2f} ms")
        print(f"FPS de processamento: {fps:.2f}")
        print("==============================")

    print("Teste finalizado.")


if __name__ == "__main__":
    main()
