from collections import defaultdict, deque


CLASSES_VEICULOS = {
    2: "carro",
    3: "moto",
    5: "onibus",
    7: "caminhao",
}


class VehicleTracker:

    def __init__(self, model, history_length=30):
        self.model = model
        self.history = defaultdict(
            lambda: deque(maxlen=history_length)
        )

    def track(self, frame):

        resultados = self.model.track(
            frame,
            persist=True,
            classes=list(CLASSES_VEICULOS.keys()),
            tracker="bytetrack.yaml",
            verbose=False,
        )

        resultado = resultados[0]

        if resultado.boxes is None:
            return resultado

        if resultado.boxes.id is None:
            return resultado

        ids = resultado.boxes.id.int().cpu().tolist()
        caixas = resultado.boxes.xyxy.cpu().tolist()

        for track_id, caixa in zip(ids, caixas):

            x1, y1, x2, y2 = map(int, caixa)

            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2

            self.history[track_id].append(
                (centro_x, centro_y)
            )

        return resultado

    def get_trajectory(self, track_id):
        return list(self.history[track_id])
