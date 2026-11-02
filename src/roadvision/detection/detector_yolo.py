from pathlib import Path
from time import perf_counter

from ultralytics import YOLO


class YOLODetector:
    """Responsável pela detecção de veículos usando YOLO."""

    CLASSES_VEICULOS = {
        2: "carro",
        3: "moto",
        5: "onibus",
        7: "caminhao",
    }

    def __init__(self, model_path=None):
        if model_path is None:
            model_path = (
                Path(__file__).resolve().parents[3]
                / "models"
                / "yolo11n.pt"
            )

        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Modelo YOLO não encontrado: {self.model_path}"
            )

        self.model = YOLO(str(self.model_path))
        self.device = "cpu"
        self.ultimo_tempo_inferencia_ms = 0.0

    def detect(self, frame):
        """Detecta veículos em um frame e registra o tempo de inferência."""

        inicio = perf_counter()

        resultados = self.model.predict(
            source=frame,
            classes=list(self.CLASSES_VEICULOS.keys()),
            device=self.device,
            verbose=False,
        )

        fim = perf_counter()
        self.ultimo_tempo_inferencia_ms = (fim - inicio) * 1000

        if not resultados:
            return None

        return resultados[0]

    def processar_frame(self, frame):
        """Retorna o resultado, o frame anotado e o tempo de inferência."""

        resultado = self.detect(frame)

        if resultado is None:
            return None, frame.copy(), self.ultimo_tempo_inferencia_ms

        frame_processado = resultado.plot()

        return (
            resultado,
            frame_processado,
            self.ultimo_tempo_inferencia_ms,
        )

    def validar_deteccoes(self, resultado):
        """Valida se as detecções pertencem às classes de veículos."""

        if resultado is None or resultado.boxes is None:
            return []

        deteccoes = []

        for caixa in resultado.boxes:
            classe_id = int(caixa.cls[0].item())

            if classe_id not in self.CLASSES_VEICULOS:
                continue

            deteccoes.append({
                "classe_id": classe_id,
                "tipo": self.CLASSES_VEICULOS[classe_id],
                "confianca": float(caixa.conf[0].item()),
            })

        return deteccoes
