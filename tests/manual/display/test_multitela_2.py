import cv2
import threading
import time

# ============================================================
# CONFIGURAÇÃO DAS CÂMERAS
# ============================================================

CAMERAS = {
    "KM 193+000 | SÃO SEBASTIÃO": 12,
    "KM 211+000 | BERTIOGA": 14,
}

BASE_URL = "http://200.144.30.103:8084/hls/cam_{}/stream.m3u8"


# ============================================================
# CLASSE PARA CAPTURAR CADA CÂMERA
# ============================================================

class Camera:
    def __init__(self, nome, camera_id):
        self.nome = nome
        self.camera_id = camera_id
        self.url = BASE_URL.format(camera_id)

        self.cap = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()

    def iniciar(self):
        print(f"🎥 Abrindo câmera: {self.nome}")
        print(f"🔗 {self.url}")

        self.cap = cv2.VideoCapture(self.url)

        if not self.cap.isOpened():
            print(f"❌ Não foi possível abrir: {self.nome}")
            return False

        print(f"✅ Câmera aberta: {self.nome}")

        self.running = True

        thread = threading.Thread(
            target=self.capturar,
            daemon=True
        )

        thread.start()

        return True

    def capturar(self):
        while self.running:

            sucesso, frame = self.cap.read()

            if sucesso:
                with self.lock:
                    self.frame = frame
            else:
                print(f"⚠️ Falha ao capturar: {self.nome}")
                time.sleep(1)

    def obter_frame(self):
        with self.lock:
            if self.frame is None:
                return None

            return self.frame.copy()

    def parar(self):
        self.running = False

        if self.cap:
            self.cap.release()


# ============================================================
# INICIANDO CÂMERAS
# ============================================================

print("=" * 70)
print("🚀 ROADVISION — TESTE MULTITELA")
print("=" * 70)

cameras = []

for nome, camera_id in CAMERAS.items():

    camera = Camera(nome, camera_id)

    if camera.iniciar():
        cameras.append(camera)

print()
print(f"📹 Câmeras abertas: {len(cameras)}/{len(CAMERAS)}")
print()

if len(cameras) == 0:
    print("❌ Nenhuma câmera conseguiu abrir.")
    exit()


# ============================================================
# AGUARDAR PRIMEIROS FRAMES
# ============================================================

print("⏳ Aguardando os primeiros frames...")

for _ in range(50):

    if all(camera.obter_frame() is not None for camera in cameras):
        break

    time.sleep(0.1)

print("✅ Frames recebidos!")
print()
print("⌨️ Pressione Q para sair.")
print()


# ============================================================
# PAINEL MULTITELA
# ============================================================

while True:

    telas = []

    for camera in cameras:

        frame = camera.obter_frame()

        if frame is None:

            frame = 255 * \
                __import__("numpy").ones(
                    (360, 640, 3),
                    dtype="uint8"
                )

            cv2.putText(
                frame,
                "SEM SINAL",
                (200, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3
            )

        else:

            # Redimensiona para o painel
            frame = cv2.resize(frame, (640, 360))

        # Nome da câmera
        cv2.rectangle(
            frame,
            (0, 0),
            (640, 40),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            camera.nome,
            (10, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        telas.append(frame)


    # ========================================================
    # ORGANIZA AS DUAS CÂMERAS LADO A LADO
    # ========================================================

    if len(telas) == 2:

        painel = cv2.hconcat(telas)

    elif len(telas) == 1:

        painel = telas[0]

    else:

        continue


    # Mostra painel
    cv2.imshow("RoadVision - Monitoramento", painel)


    # Q encerra
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        break


# ============================================================
# ENCERRAMENTO
# ============================================================

print()
print("🛑 Encerrando...")

for camera in cameras:
    camera.parar()

cv2.destroyAllWindows()

print("✅ Teste finalizado!")