import cv2
import time
import threading
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

# Processa aproximadamente 1 frame por segundo por câmera
INTERVALO_ANALISE = 1.0

# Classes COCO que nos interessam
CLASSES_VEICULOS = {
    2: "carro",
    3: "moto",
    5: "ônibus",
    7: "caminhão",
}


# ============================================================
# CLASSE DA CÂMERA
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

        self.frames_recebidos = 0
        self.online = False

    def iniciar(self):

        print(f"🎥 Abrindo ID {self.camera_id} | {self.nome}")

        self.cap = cv2.VideoCapture(self.url)

        if not self.cap.isOpened():

            print(f"❌ Não abriu ID {self.camera_id}")

            return False

        self.running = True
        self.online = True

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
                    self.frames_recebidos += 1

            else:

                time.sleep(0.5)

    def obter_frame(self):

        with self.lock:

            if self.frame is None:
                return None

            return self.frame.copy()

    def parar(self):

        self.running = False
        self.online = False

        if self.cap:
            self.cap.release()


# ============================================================
# CARREGAR YOLO
# ============================================================

print("=" * 70)
print("🚀 ROADVISION — 11 CÂMERAS + YOLO SEM TELA")
print("=" * 70)

print()
print("🤖 Carregando YOLO...")

model = YOLO("yolo11n.pt")

print("✅ Modelo carregado!")
print()


# ============================================================
# ABRIR CÂMERAS
# ============================================================

cameras = []

for camera_id, nome in CAMERAS:

    camera = Camera(camera_id, nome)

    if camera.iniciar():
        cameras.append(camera)


print()
print("=" * 70)
print(f"📹 Câmeras conectadas: {len(cameras)}/{len(CAMERAS)}")
print("=" * 70)

print()
print("⏳ Aguardando frames...")
time.sleep(5)

print()
print("🧠 Iniciando YOLO...")
print("⌨️ Pressione CTRL+C para encerrar.")
print()


# ============================================================
# CONTADORES
# ============================================================

ultima_analise = {}

total_processamentos = 0
inicio = time.time()


# ============================================================
# PROCESSAMENTO
# ============================================================

try:

    while True:

        agora = time.time()

        for camera in cameras:

            # Controle da frequência de análise
            ultima = ultima_analise.get(
                camera.camera_id,
                0
            )

            if agora - ultima < INTERVALO_ANALISE:
                continue

            frame = camera.obter_frame()

            if frame is None:
                continue

            ultima_analise[camera.camera_id] = agora

            # Reduz o tamanho antes de mandar para o YOLO
            frame_pequeno = cv2.resize(
                frame,
                (640, 360)
            )

            # =================================================
            # YOLO
            # =================================================

            resultado = model.predict(
                frame_pequeno,
                imgsz=640,
                conf=0.40,
                verbose=False
            )[0]

            contagem = {
                "carro": 0,
                "moto": 0,
                "ônibus": 0,
                "caminhão": 0,
            }

            # =================================================
            # CONTAR DETECÇÕES
            # =================================================

            if resultado.boxes is not None:

                for classe in resultado.boxes.cls:

                    classe_id = int(classe)

                    if classe_id in CLASSES_VEICULOS:

                        tipo = CLASSES_VEICULOS[classe_id]

                        contagem[tipo] += 1

            total = sum(contagem.values())

            print(
                f"📹 ID {camera.camera_id:02d} | "
                f"{camera.nome:<32} | "
                f"🚗 {contagem['carro']} | "
                f"🏍️ {contagem['moto']} | "
                f"🚌 {contagem['ônibus']} | "
                f"🚚 {contagem['caminhão']} | "
                f"TOTAL {total}"
            )

            total_processamentos += 1


        # =====================================================
        # STATUS GERAL A CADA 10 SEGUNDOS
        # =====================================================

        if int(agora - inicio) % 10 == 0:

            tempo = agora - inicio

            if tempo > 0:

                fps_processamento = (
                    total_processamentos / tempo
                )

                print()
                print("-" * 70)
                print(
                    f"📊 STATUS | "
                    f"Tempo: {int(tempo)}s | "
                    f"Análises YOLO: {total_processamentos} | "
                    f"Taxa: {fps_processamento:.2f} análises/s"
                )

                print("-" * 70)
                print()


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
print("📊 RESULTADO FINAL")
print("=" * 70)

print(f"🎥 Câmeras abertas: {len(cameras)}/{len(CAMERAS)}")
print(f"🧠 Análises realizadas: {total_processamentos}")

print()
print("✅ Teste finalizado!")