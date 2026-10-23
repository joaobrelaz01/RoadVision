
from roadvision.detection.contagem_linha_virtual import (
    SENTIDO_1,
    SENTIDO_2,
    LinhaVirtualContagem,
)


class IdentificadorSentido:
    """Identifica o sentido usando a trajetória de um veículo."""

    def __init__(self, linha_virtual: LinhaVirtualContagem):
        self.linha_virtual = linha_virtual

    def identificar(self, trajetoria):
        """Retorna o sentido do cruzamento ou None se não identificado."""

        if not trajetoria or len(trajetoria) < 2:
            return None

        inicio = self.linha_virtual.ponto_inicial
        fim = self.linha_virtual.ponto_final

        for anterior, atual in zip(trajetoria, trajetoria[1:]):
            anterior = self.linha_virtual._validar_ponto(anterior)
            atual = self.linha_virtual._validar_ponto(atual)

            lado_anterior = self.linha_virtual._orientacao(
                inicio, fim, anterior
            )
            lado_atual = self.linha_virtual._orientacao(
                inicio, fim, atual
            )

            # Ignora pontos sobre a linha ou sem mudança de lado.
            if lado_anterior * lado_atual >= 0:
                continue

            if not self.linha_virtual._segmentos_intersectam(
                anterior, atual, inicio, fim
            ):
                continue

            if lado_anterior < 0 < lado_atual:
                return SENTIDO_1

            return SENTIDO_2

        return None
