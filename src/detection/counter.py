class VirtualLineCounter:
    def __init__(self, ponto_inicial, ponto_final):
        self.ponto_inicial = ponto_inicial
        self.ponto_final = ponto_final
        self.posicoes_anteriores = {}
        self.veiculos_contados = set()

    def calcular_lado(self, ponto):
        x1, y1 = self.ponto_inicial
        x2, y2 = self.ponto_final
        x, y = ponto

        resultado = (
            (x2 - x1) * (y - y1)
            - (y2 - y1) * (x - x1)
        )

        if resultado > 0:
            return 1
        elif resultado < 0:
            return -1
        return 0

    def atualizar(self, track_id, centroide):
        if track_id is None:
            return None

        lado_atual = self.calcular_lado(centroide)

        # Ignora pontos exatamente sobre a linha
        if lado_atual == 0:
            return None

        lado_anterior = self.posicoes_anteriores.get(track_id)
        self.posicoes_anteriores[track_id] = lado_atual

        if lado_anterior is None:
            return None

        if track_id in self.veiculos_contados:
            return None

        if lado_anterior != lado_atual:
            self.veiculos_contados.add(track_id)

            if lado_anterior < lado_atual:
                return "sentido_positivo"

            return "sentido_negativo"

        return None

    def calcular_centroide(self, caixa):
        x1, y1, x2, y2 = caixa
        return ((x1 + x2) / 2, (y1 + y2) / 2)
