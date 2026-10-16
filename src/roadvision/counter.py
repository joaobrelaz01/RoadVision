
class VehicleCounter:
    """Gerencia a contagem única de veículos rastreados."""

    def __init__(self):
        self.counted_ids = set()
        self.count_by_direction = {}

    def registrar_cruzamento(self, track_id, direction=None):
        """Registra um veículo uma única vez.

        Retorna True quando o ID é contado pela primeira vez
        e False quando ele já foi contabilizado.
        """
        if track_id is None or track_id in self.counted_ids:
            return False

        self.counted_ids.add(track_id)

        if direction is not None:
            self.count_by_direction[direction] = (
                self.count_by_direction.get(direction, 0) + 1
            )

        return True

    def total_contado(self):
        """Retorna a quantidade total de veículos contabilizados."""
        return len(self.counted_ids)

    def total_por_sentido(self, direction):
        """Retorna a quantidade contabilizada em um sentido."""
        return self.count_by_direction.get(direction, 0)
