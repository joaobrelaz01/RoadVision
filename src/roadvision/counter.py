
from roadvision.detection.contagem_linha_virtual import (
    SENTIDO_1,
    SENTIDO_2,
)

CATEGORIAS_VEICULOS = ("carro", "moto", "onibus", "caminhao")
SENTIDOS_VALIDOS = (SENTIDO_1, SENTIDO_2)


class VehicleCounter:
    """Conta veículos únicos por tipo e sentido."""

    def __init__(self):
        self.counted_ids = set()
        self.count_by_direction = {
            sentido: 0 for sentido in SENTIDOS_VALIDOS
        }
        self.count_by_type = {
            tipo: 0 for tipo in CATEGORIAS_VEICULOS
        }
        self.vehicle_types = {}
        self.vehicle_directions = {}

    def registrar_cruzamento(
        self, track_id, direction=None, vehicle_type=None
    ):
        """Registra um veículo uma única vez."""
        if track_id is None or track_id in self.counted_ids:
            return False

        if direction is not None and direction not in SENTIDOS_VALIDOS:
            raise ValueError(f"Sentido inválido: {direction}")

        if (
            vehicle_type is not None
            and vehicle_type not in CATEGORIAS_VEICULOS
        ):
            raise ValueError(f"Tipo de veículo inválido: {vehicle_type}")

        if direction is None and vehicle_type is None:
            return False

        self.counted_ids.add(track_id)

        if direction is not None:
            self.count_by_direction[direction] += 1
            self.vehicle_directions[track_id] = direction

        if vehicle_type is not None:
            self.vehicle_types[track_id] = vehicle_type
            self.count_by_type[vehicle_type] += 1

        return True

    def total_contado(self):
        return len(self.counted_ids)

    def total_por_sentido(self, direction):
        if direction not in SENTIDOS_VALIDOS:
            raise ValueError(f"Sentido inválido: {direction}")
        return self.count_by_direction[direction]

    def resumo_por_sentido(self):
        return self.count_by_direction.copy()

    def total_por_tipo(self, vehicle_type):
        if vehicle_type not in CATEGORIAS_VEICULOS:
            raise ValueError(f"Tipo de veículo inválido: {vehicle_type}")
        return self.count_by_type[vehicle_type]

    def resumo_por_tipo(self):
        return self.count_by_type.copy()
