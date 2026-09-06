import cv2
from ultralytics import YOLO


# ============================================================
# CONFIGURAÇÕES
# ============================================================

STREAM_URL = "http://200.144.30.103:8084/hls/cam_14/stream.m3u8"

# Modelo pequeno para o primeiro teste
MODEL_PATH = "yolo11n.pt"


# ============================================================
# CARREGAR MODELO
# ============================================================

print("🤖 Carregando modelo YOLO...")

model = YOLO(MODEL_PATH)

print("✅ Modelo carregado!")


# ============================================================
# ABRIR CÂMERA
# ============================================================

print("\n🎥 Abrindo câmera...")

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("❌ Não foi possível abrir o stream.")
    exit()

print("✅ Stream aberto!")


# ============================================================
# PROCESSAMENTO
# ============================================================

print("\n🧠 Iniciando detecção...")
print("Pressione Q para sair.\n")


while True:

    sucesso, frame = cap.read()

    if not sucesso:
        print("⚠️ Não foi possível capturar frame.")
        break

    # YOLO analisa o frame
    resultados = model(
        frame,
        verbose=False
    )

    # Desenha as detecções
    frame_analisado = resultados[0].plot()

    # Mostra resultado
    cv2.imshow(
        "RoadVision - YOLO - Camera 8",
        frame_analisado
    )

    # Aperte Q para sair
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# FINALIZAÇÃO
# ============================================================

cap.release()
cv2.destroyAllWindows()

print("\n🏁 Teste finalizado!")