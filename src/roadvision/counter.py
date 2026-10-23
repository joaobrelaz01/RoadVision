
CATEGORIAS_VEICULOS = ("carro", "moto", "onibus", "caminhao")


class VehicleCounter:
    """Conta veículos únicos por tipo e sentido."""

    def __init__(self):
        self.counted_ids = set()
        self.count_by_direction = {}
        self.count_by_type = {
            tipo: 0 for tipo in CATEGORIAS_VEICULOS
        }
        self.vehicle_types = {}

    def registrar_cruzamento(
        self, track_id, direction=None, vehicle_type=None
    ):
        """Registra um veículo uma única vez."""
        if track_id is None or track_id in self.counted_ids:
            return False

        if (
            vehicle_type is not None
            and vehicle_type not in CATEGORIAS_VEICULOS
        ):
            raise ValueError(f"Tipo de veículo inválido: {vehicle_type}")

        self.counted_ids.add(track_id)

        if direction is not None:
            self.count_by_direction[direction] = (
                self.count_by_direction.get(direction, 0) + 1
            )

        if vehicle_type is not None:
            self.vehicle_types[track_id] = vehicle_type
            self.count_by_type[vehicle_type] += 1

        return True

    def total_contado(self):
        return len(self.counted_ids)

    def total_por_sentido(self, direction):
        return self.count_by_direction.get(direction, 0)

    def total_por_tipo(self, vehicle_type):
        if vehicle_type not in CATEGORIAS_VEICULOS:
            raise ValueError(f"Tipo de veículo inválido: {vehicle_type}")
        return self.count_by_type[vehicle_type]

    def resumo_por_tipo(self):
        return self.count_by_type.copy()
