import cv2
import time
import threading
from collections import defaultdict
from ultralytics import YOLO


# ============================================================
# CONFIGURAÇÃO
# ============================================================

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

# Uma análise por câmera a cada ciclo
INTERVALO_ANALISE = 2.0

CLASSES_VEICULOS = {
    2: "carro",
    3: "moto",
    5: "onibus",
    7: "caminhao",
}


# ============================================================
# CÂMERA
# ============================================================

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

        print(
            f"🎥 Conectando ID {self.camera_id:02d} | "
            f"{self.nome}"
        )

        self.cap = cv2.VideoCapture(self.url)

        if not self.cap.isOpened():

            print(
                f"❌ Falha ID {self.camera_id:02d}"
            )

            return False

        self.running = True

        thread = threading.Thread(
            target=self.capturar,
            daemon=True
        )

        thread.start()

        print(
            f"✅ ID {self.camera_id:02d} conectado"
        )

        return True

    def capturar(self):

        while self.running:

            try:

                sucesso, frame = self.cap.read()

                if sucesso:

                    with self.lock:
                        self.frame = frame

                else:

                    time.sleep(0.2)

            except cv2.error:

                # Evita que uma falha de H264 derrube o programa
                time.sleep(0.5)

    def obter_frame(self):

        with self.lock:

            if self.frame is None:
                return None

            return self.frame.copy()

    def parar(self):

        self.running = False

        if self.cap:

            try:
                self.cap.release()
            except:
                pass


# ============================================================
# INÍCIO
# ============================================================

print("=" * 70)
print("🚀 ROADVISION")
print("🤖 11 CÂMERAS + YOLO")
print("⚡ PROCESSAMENTO SEQUENCIAL")
print("📊 SEM TELA")
print("=" * 70)

print()
print("🤖 Carregando YOLO...")

model = YOLO("yolo11n.pt")

print("✅ Modelo carregado!")
print()


# ============================================================
# CONECTAR CÂMERAS
# ============================================================

cameras = []

for camera_id, nome in CAMERAS:

    camera = Camera(camera_id, nome)

    if camera.iniciar():
        cameras.append(camera)


print()
print(
    f"📹 Câmeras conectadas: "
    f"{len(cameras)}/{len(CAMERAS)}"
)

print()
print("⏳ Aguardando frames...")
time.sleep(5)

print()
print("🧠 Processamento iniciado!")
print("⌨️ CTRL+C para encerrar.")
print()


# ============================================================
# CONTADORES DO MINUTO
# ============================================================

contagem_minuto = defaultdict(
    lambda: {
        "carro": 0,
        "moto": 0,
        "onibus": 0,
        "caminhao": 0,
    }
)

inicio_minuto = time.time()

total_analises = 0


# ============================================================
# LOOP
# ============================================================

try:

    while True:

        for camera in cameras:

            frame = camera.obter_frame()

            if frame is None:
                continue

            # Reduz resolução
            frame = cv2.resize(
                frame,
                (640, 360)
            )

            # =================================================
            # YOLO — DETECÇÃO, NÃO TRACKING
            # =================================================

            resultado = model.predict(
                frame,
                imgsz=640,
                conf=0.40,
                verbose=False
            )[0]

            if resultado.boxes is None:
                continue

            # =================================================
            # CONTAR OBJETOS DETECTADOS NO FRAME
            # =================================================

            for classe in resultado.boxes.cls:

                classe_id = int(classe)

                if classe_id in CLASSES_VEICULOS:

                    tipo = CLASSES_VEICULOS[classe_id]

                    contagem_minuto[
                        camera.camera_id
                    ][tipo] += 1

            total_analises += 1


        # =====================================================
        # FECHAMENTO DO MINUTO
        # =====================================================

        agora = time.time()

        if agora - inicio_minuto >= 60:

            print()
            print("=" * 70)
            print("📊 RESUMO DO MINUTO")
            print("=" * 70)

            total_geral = 0

            for camera in cameras:

                dados = contagem_minuto[
                    camera.camera_id
                ]

                total = sum(
                    dados.values()
                )

                total_geral += total

                print()
                print(
                    f"📹 ID {camera.camera_id:02d} | "
                    f"{camera.nome}"
                )

                print(
                    f"   🚗 Carros:    "
                    f"{dados['carro']}"
                )

                print(
                    f"   🏍️ Motos:     "
                    f"{dados['moto']}"
                )

                print(
                    f"   🚌 Ônibus:   "
                    f"{dados['onibus']}"
                )

                print(
                    f"   🚚 Caminhões: "
                    f"{dados['caminhao']}"
                )

                print(
                    f"   🚘 TOTAL:     "
                    f"{total}"
                )


            print()
            print("-" * 70)

            print(
                f"🚘 TOTAL GERAL: {total_geral}"
            )

            print(
                f"🧠 Análises YOLO: "
                f"{total_analises}"
            )

            print("-" * 70)


            # Novo minuto
            contagem_minuto.clear()

            inicio_minuto = time.time()


        time.sleep(0.01)


except KeyboardInterrupt:

    print()
    print("🛑 Encerrando manualmente...")


# ============================================================
# ENCERRAMENTO
# ============================================================

for camera in cameras:

    camera.parar()


print()
print("=" * 70)
print("🏁 ROADVISION ENCERRADO")
print("=" * 70)