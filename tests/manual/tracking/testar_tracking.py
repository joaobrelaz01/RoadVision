import time
from pathlib import Path
import cv2
from ultralytics import YOLO

from roadvision.ia.tracker import VehicleTracker


STREAM_URL = "http://200.144.30.103:8084/hls/cam_14/stream.m3u8"

MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "yolo11n.pt"


print("Carregando modelo YOLO...")
model = YOLO(MODEL_PATH)

tracker = VehicleTracker(model)

print("Abrindo camera...")
cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Nao foi possivel abrir a camera.")
    raise SystemExit


inicio = time.perf_counter()
frames_processados = 0
frame_atual = 0
ultimo_log = inicio

ids_vistos = set()
ultimo_frame_id = {}


while True:

    sucesso, frame = cap.read()

    if not sucesso:
        print("Falha ao capturar frame.")
        break

    frame_atual += 1

    frame = cv2.resize(frame, (640, 360))

    resultado = tracker.track(frame)

    frames_processados += 1

    # IDs ativos neste frame
    ids_ativos = []

    if resultado.boxes is not None and resultado.boxes.id is not None:
        ids_ativos = resultado.boxes.id.int().cpu().tolist()

    # Identifica novos veículos e possíveis oclusões
    for track_id in ids_ativos:

        if track_id not in ids_vistos:
            print(f"Novo veiculo detectado - ID: {track_id}")
            ids_vistos.add(track_id)

        if track_id in ultimo_frame_id:

            intervalo = frame_atual - ultimo_frame_id[track_id]

            if intervalo > 1:
                print(
                    f"Oclusao/ausencia detectada - "
                    f"ID {track_id} voltou apos {intervalo} frames"
                )

        ultimo_frame_id[track_id] = frame_atual

    # Exibe FPS e IDs a cada 5 segundos
    agora = time.perf_counter()

    if agora - ultimo_log >= 5:

        tempo_total = agora - inicio
        fps_medio = frames_processados / tempo_total

        print(
            f"FPS medio: {fps_medio:.2f} | "
            f"IDs ativos: {ids_ativos} | "
            f"Total de IDs vistos: {len(ids_vistos)}"
        )

        ultimo_log = agora

    # Desenha caixas e IDs do YOLO/ByteTrack
    frame_analisado = resultado.plot()

    # Desenha somente as trajetórias dos veículos atualmente ativos
    for track_id in ids_ativos:

        pontos = tracker.history.get(track_id, [])

        if len(pontos) < 2:
            continue

        for i in range(1, len(pontos)):

            cv2.line(
                frame_analisado,
                pontos[i - 1],
                pontos[i],
                (255, 0, 0),
                2,
            )

    cv2.imshow(
        "RoadVision - Tracking",
        frame_analisado
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()


tempo_total = time.perf_counter() - inicio

if tempo_total > 0:

    fps_final = frames_processados / tempo_total

    print(f"FPS medio final: {fps_final:.2f}")


print(f"Total de frames processados: {frames_processados}")
print(f"Total de veiculos rastreados: {len(ids_vistos)}")
print("Teste de tracking finalizado.")