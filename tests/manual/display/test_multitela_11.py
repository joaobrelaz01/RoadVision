import cv2
import threading
import time
import numpy as np


CAMERAS = [
    (36, "KM 055+000 | MARANDUBA"),
    (5, "KM 073+000 | MARANDUBA"),
    (38, "KM 083+500 | MARANDUBA"),
    (37, "KM 092+500 | CARAGUATATUBA"),
    (8, "KM 110+000 | SÃO SEBASTIÃO"),
    (9, "KM 110+000 | MASSAGUAÇU"),
    (10, "KM 136+000 | CARAGUATATUBA"),
    (11, "KM 168+000 | BERTIOGA"),
    (12, "KM 193+000 | SÃO SEBASTIÃO"),
    (13, "KM 211+000 | SÃO SEBASTIÃO"),
    (14, "KM 211+000 | BERTIOGA"),
]

BASE_URL = "http://200.144.30.103:8084/hls/cam_{}/stream.m3u8"

LARGURA = 480
ALTURA = 270


class Camera:

    def __init__(self, camera_id, nome):

        self.camera_id = camera_id
        self.nome = nome
        self.url = BASE_URL.format(camera_id)

        self.cap = None
        self.frame = None
        self.running = False

        self.lock = threading.Lock()

    def iniciar(self):

        print(f"🎥 Abrindo ID {self.camera_id} | {self.nome}")

        self.cap = cv2.VideoCapture(self.url)

        if not self.cap.isOpened():

            print(f"❌ Falha ID {self.camera_id}")

            return False

        self.running = True

        thread = threading.Thread(
            target=self.capturar,
            daemon=True
        )

        thread.start()

        print(f"✅ ID {self.camera_id} conectado")

        return True

    def capturar(self):

        while self.running:

            sucesso, frame = self.cap.read()

            if sucesso:

                with self.lock:
                    self.frame = frame

            else:

                time.sleep(0.5)

    def obter_frame(self):

        with self.lock:

            if self.frame is None:
                return None

            return self.frame.copy()

    def parar(self):

        self.running = False

        if self.cap:
            self.cap.release()


print("=" * 70)
print("🚀 ROADVISION — TESTE MULTITELA 11 CÂMERAS")
print("=" * 70)

cameras = []

for camera_id, nome in CAMERAS:

    camera = Camera(camera_id, nome)

    if camera.iniciar():
        cameras.append(camera)

print()
print(f"📹 Câmeras conectadas: {len(cameras)}/{len(CAMERAS)}")
print()

print("⏳ Aguardando frames...")

time.sleep(5)

print("✅ Iniciando painel!")
print("⌨️ Pressione Q para sair.")


while True:

    telas = []

    for camera in cameras:

        frame = camera.obter_frame()

        if frame is None:

            frame = np.zeros(
                (ALTURA, LARGURA, 3),
                dtype=np.uint8
            )

            cv2.putText(
                frame,
                "SEM SINAL",
                (130, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        else:

            frame = cv2.resize(
                frame,
                (LARGURA, ALTURA)
            )

        # Barra superior
        cv2.rectangle(
            frame,
            (0, 0),
            (LARGURA, 35),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            f"ID {camera.camera_id} | {camera.nome}",
            (8, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1
        )

        telas.append(frame)


    # Completa com telas vazias caso alguma câmera falhe
    while len(telas) < 12:

        telas.append(
            np.zeros(
                (ALTURA, LARGURA, 3),
                dtype=np.uint8
            )
        )


    # Monta grade 4 x 3

    linha1 = cv2.hconcat(telas[0:4])
    linha2 = cv2.hconcat(telas[4:8])
    linha3 = cv2.hconcat(telas[8:12])

    painel = cv2.vconcat([
        linha1,
        linha2,
        linha3
    ])


    cv2.imshow(
        "RoadVision - 11 Cameras",
        painel
    )


    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        break


print()
print("🛑 Encerrando câmeras...")

for camera in cameras:
    camera.parar()

cv2.destroyAllWindows()

print("✅ Teste finalizado!")