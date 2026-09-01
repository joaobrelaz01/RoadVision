import cv2
from ultralytics import YOLO

CAMERA_ID = 14

URL = f"http://200.144.30.103:8084/hls/cam_{CAMERA_ID}/stream.m3u8"

print("🤖 Carregando YOLO...")

model = YOLO("yolo11n.pt")

print("✅ Modelo carregado!")

print("🎥 Abrindo câmera...")

cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("❌ Não conseguiu abrir a câmera.")
    exit()

print("✅ Câmera aberta!")

print()
print("🧠 Procurando objetos...")
print("⌨️ Pressione Q para sair.")
print()

while True:

    sucesso, frame = cap.read()

    if not sucesso:
        continue

    # Mantemos uma resolução razoável
    frame = cv2.resize(frame, (960, 540))

    resultado = model.predict(
        frame,
        imgsz=960,
        conf=0.20,
        verbose=False
    )[0]

    encontrados = {}

    if resultado.boxes is not None:

        for classe, confianca in zip(
            resultado.boxes.cls,
            resultado.boxes.conf
        ):

            classe_id = int(classe)
            confianca = float(confianca)

            nome = model.names[classe_id]

            if nome not in encontrados:
                encontrados[nome] = []

            encontrados[nome].append(confianca)

    print("\033[2J\033[H", end="")

    print("=" * 60)
    print("🔎 OBJETOS DETECTADOS")
    print("=" * 60)

    if not encontrados:

        print("Nenhum objeto detectado.")

    else:

        for nome, confiancas in sorted(encontrados.items()):

            maior = max(confiancas)

            print(
                f"{nome:<15} "
                f"quantidade: {len(confiancas):<3} "
                f"confiança máxima: {maior:.2f}"
            )

    cv2.imshow(
        "Teste de classes YOLO",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

print()
print("🏁 Teste encerrado.")