import cv2
from ultralytics import YOLO
import time


STREAM_URL = "http://200.144.30.103:8084/hls/cam_12/stream.m3u8"
MODEL_PATH = "yolo11n.pt"

VEICULOS = {
    2: "carro",
    3: "moto",
    5: "onibus",
    7: "caminhao",
}

print("🤖 Carregando YOLO...")
model = YOLO(MODEL_PATH)
print("✅ Modelo carregado!")

print("🎥 Abrindo câmera 12...")
cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("❌ Não foi possível abrir o stream.")
    exit()

print("✅ Stream aberto!")
print("🧠 Iniciando processamento sem tela...")
print("⌨️ Pressione CTRL+C para encerrar.\n")


ids_contados = set()
contador = 0

inicio = time.time()
frames = 0


try:

    while True:

        sucesso, frame = cap.read()

        if not sucesso:
            print("⚠️ Falha ao capturar frame.")
            break

        frames += 1

        altura, largura = frame.shape[:2]

        # Linha imaginária no meio da imagem
        linha_y = altura // 2

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

                if classe not in VEICULOS:
                    continue

                x1, y1, x2, y2 = map(int, caixa)

                centro_y = (y1 + y2) // 2

                nome = VEICULOS[classe]

                # Verifica se o veículo cruzou a linha
                if linha_y - 5 <= centro_y <= linha_y + 5:

                    if track_id not in ids_contados:

                        ids_contados.add(track_id)
                        contador += 1

                        print(
                            f"🚗 Veículo detectado | "
                            f"ID: {track_id} | "
                            f"Tipo: {nome} | "
                            f"Total: {contador}"
                        )


        # Mostra estatísticas a cada 30 segundos
        tempo = time.time() - inicio

        if tempo >= 30:

            fps = frames / tempo

            print(
                f"\n📊 STATUS | "
                f"Tempo: {tempo:.0f}s | "
                f"Frames: {frames} | "
                f"FPS médio: {fps:.2f} | "
                f"Veículos: {contador}\n"
            )

            inicio = time.time()
            frames = 0


except KeyboardInterrupt:

    print("\n🛑 Encerrando manualmente...")


finally:

    cap.release()

    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)

    print(f"🚗 Veículos contabilizados: {contador}")
    print("🏁 Teste encerrado.")