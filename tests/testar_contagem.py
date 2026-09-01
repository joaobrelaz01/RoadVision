import cv2
from ultralytics import YOLO


STREAM_URL = "http://200.144.30.103:8084/hls/cam_12/stream.m3u8"

MODEL_PATH = "yolo11n.pt"

# Classes que queremos considerar como veículos
VEICULOS = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}


print("🤖 Carregando YOLO...")

model = YOLO(MODEL_PATH)

print("✅ Modelo carregado!")

print("🎥 Abrindo câmera...")

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("❌ Não foi possível abrir o stream.")
    exit()

print("✅ Stream aberto!")

# IDs que já foram contabilizados
ids_contados = set()

contador = 0


while True:

    sucesso, frame = cap.read()

    if not sucesso:
        print("⚠️ Falha ao capturar frame.")
        break

    altura, largura = frame.shape[:2]

    # Linha de contagem
    linha_y = altura // 2

    # Tracking
    resultados = model.track(
        frame,
        persist=True,
        verbose=False,
        tracker="bytetrack.yaml"
    )

    resultado = resultados[0]

    if resultado.boxes.id is not None:

        ids = resultado.boxes.id.int().cpu().tolist()

        classes = resultado.boxes.cls.int().cpu().tolist()

        caixas = resultado.boxes.xyxy.cpu().tolist()

        for track_id, classe, caixa in zip(
            ids,
            classes,
            caixas
        ):

            # Ignorar objetos que não são veículos
            if classe not in VEICULOS:
                continue

            x1, y1, x2, y2 = map(int, caixa)

            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2

            nome = VEICULOS[classe]

            # Desenhar caixa
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Mostrar ID
            cv2.putText(
                frame,
                f"{nome} ID:{track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # Verificar cruzamento da linha
            if (
                linha_y - 5
                <= centro_y
                <= linha_y + 5
            ):

                if track_id not in ids_contados:

                    ids_contados.add(track_id)

                    contador += 1

                    print(
                        f"🚗 Veículo contabilizado! "
                        f"ID={track_id} "
                        f"Tipo={nome} "
                        f"Total={contador}"
                    )

            # Centro do veículo
            cv2.circle(
                frame,
                (centro_x, centro_y),
                4,
                (255, 0, 0),
                -1
            )

    # Linha de contagem
    cv2.line(
        frame,
        (0, linha_y),
        (largura, linha_y),
        (255, 0, 0),
        2
    )

    # Contador
    cv2.putText(
        frame,
        f"Veiculos: {contador}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "RoadVision - Contagem",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()

print("\n🏁 Teste finalizado!")
print(f"🚗 Total de veículos contabilizados: {contador}")