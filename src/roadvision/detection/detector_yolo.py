from pathlib import Path

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

        self.model = YOLO(self.model_path)

    def detect(self, frame):
        """Executa a detecção de veículos em um frame."""

        resultados = self.model.predict(
            frame,
            classes=list(self.CLASSES_VEICULOS.keys()),
            verbose=False,
        )

        return resultados[0]