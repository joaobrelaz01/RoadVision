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

INTERVALO_ANALISE = 1.0

# Classes de veículos do modelo COCO
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
                f"❌ Falha ao conectar ID {self.camera_id:02d}"
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


# ============================================================
# INICIAR
# ============================================================

print("=" * 70)
print("🚀 ROADVISION")
print("🤖 11 CÂMERAS + YOLO TRACKING")
print("📊 CONTAGEM POR MINUTO")
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
print("⏳ Aguardando streams...")
time.sleep(5)

print()
print("🧠 Iniciando processamento...")
print("⌨️ CTRL+C para encerrar")
print()


# ============================================================
# DADOS DO TRACKING
# ============================================================

# IDs que já foram contabilizados naquele minuto
contabilizados = defaultdict(set)

# Contadores por câmera
contagem = defaultdict(
    lambda: {
        "carro": 0,
        "moto": 0,
        "onibus": 0,
        "caminhao": 0,
    }
)

ultima_analise = {}

inicio_minuto = time.time()

total_analises = 0


# ============================================================
# LOOP PRINCIPAL
# ============================================================

try:

    while True:

        agora = time.time()


        # ====================================================
        # ANALISAR CÂMERAS
        # ====================================================

        for camera in cameras:

            camera_id = camera.camera_id

            ultima = ultima_analise.get(
                camera_id,
                0
            )

            if agora - ultima < INTERVALO_ANALISE:
                continue

            frame = camera.obter_frame()

            if frame is None:
                continue

            ultima_analise[camera_id] = agora


            # Reduz resolução para aliviar CPU
            frame = cv2.resize(
                frame,
                (640, 360)
            )


            # =================================================
            # YOLO TRACKING
            # =================================================

            resultado = model.track(
                frame,
                persist=True,
                imgsz=640,
                conf=0.40,
                verbose=False
            )[0]


            if resultado.boxes is None:
                continue


            # =================================================
            # PROCESSAR OBJETOS
            # =================================================

            if resultado.boxes.id is None:
                continue


            ids = resultado.boxes.id.cpu().tolist()

            classes = (
                resultado.boxes.cls
                .cpu()
                .tolist()
            )


            for tracker_id, classe_id in zip(
                ids,
                classes
            ):

                tracker_id = int(tracker_id)
                classe_id = int(classe_id)


                if classe_id not in CLASSES_VEICULOS:
                    continue


                tipo = CLASSES_VEICULOS[classe_id]


                # =================================================
                # EVITAR DUPLICAÇÃO
                # =================================================

                if tracker_id in contabilizados[camera_id]:
                    continue


                contabilizados[camera_id].add(
                    tracker_id
                )


                contagem[camera_id][tipo] += 1


            total_analises += 1


        # ====================================================
        # FECHAR MINUTO
        # ====================================================

        if agora - inicio_minuto >= 60:

            print()
            print("=" * 70)

            minuto = int(
                (agora - inicio_minuto) / 60
            )

            print("📊 ROADVISION — RESUMO")
            print("=" * 70)


            total_geral = 0


            for camera in cameras:

                dados = contagem[
                    camera.camera_id
                ]


                total_camera = sum(
                    dados.values()
                )


                total_geral += total_camera


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
                    f"{total_camera}"
                )


            print()
            print("-" * 70)

            print(
                f"🚘 TOTAL DAS 11 CÂMERAS: "
                f"{total_geral}"
            )

            print("-" * 70)


            # =================================================
            # NOVO MINUTO
            # =================================================

            contabilizados.clear()
            contagem.clear()

            inicio_minuto = time.time()


        time.sleep(0.01)


except KeyboardInterrupt:

    print()
    print("🛑 Encerrando...")


# ============================================================
# FINALIZAÇÃO
# ============================================================

for camera in cameras:
    camera.parar()


print()
print("=" * 70)
print("🏁 ROADVISION ENCERRADO")
print("=" * 70)