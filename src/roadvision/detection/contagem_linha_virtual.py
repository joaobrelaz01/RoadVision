
class LinhaVirtualContagem:
    """Detecta cruzamentos de veículos por um segmento virtual."""

    def __init__(self, ponto_inicial, ponto_final):
        self.ponto_inicial = self._validar_ponto(ponto_inicial)
        self.ponto_final = self._validar_ponto(ponto_final)

        if self.ponto_inicial == self.ponto_final:
            raise ValueError("A linha precisa ter dois pontos diferentes.")

        self.ids_contados = set()

    @staticmethod
    def _validar_ponto(ponto):
        if (
            not isinstance(ponto, (tuple, list))
            or len(ponto) != 2
            or any(
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                for valor in ponto
            )
        ):
            raise ValueError(
                "O ponto deve conter coordenadas numéricas (x, y)."
            )

        return tuple(ponto)

    @staticmethod
    def _orientacao(a, b, c):
        return (
            (b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0])
        )

    @staticmethod
    def _estao_em_segmento(a, b, ponto):
        return (
            min(a[0], b[0]) <= ponto[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= ponto[1] <= max(a[1], b[1])
        )

    @classmethod
    def _segmentos_intersectam(cls, a, b, c, d):
        o1 = cls._orientacao(a, b, c)
        o2 = cls._orientacao(a, b, d)
        o3 = cls._orientacao(c, d, a)
        o4 = cls._orientacao(c, d, b)

        if (
            ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0))
            and ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0))
        ):
            return True

        if o1 == 0 and cls._estao_em_segmento(a, b, c):
            return True
        if o2 == 0 and cls._estao_em_segmento(a, b, d):
            return True
        if o3 == 0 and cls._estao_em_segmento(c, d, a):
            return True
        if o4 == 0 and cls._estao_em_segmento(c, d, b):
            return True

        return False

    def verificar_cruzamento(
        self, track_id, ponto_anterior, ponto_atual
    ):
        """Retorna o sentido geométrico ou None, sem duplicar IDs."""

        if track_id in self.ids_contados:
            return None

        anterior = self._validar_ponto(ponto_anterior)
        atual = self._validar_ponto(ponto_atual)

        inicio = self.ponto_inicial
        fim = self.ponto_final

        lado_anterior = self._orientacao(inicio, fim, anterior)
        lado_atual = self._orientacao(inicio, fim, atual)

        if lado_anterior * lado_atual >= 0:
            return None

        if not self._segmentos_intersectam(
            anterior, atual, inicio, fim
        ):
            return None

        self.ids_contados.add(track_id)

        if lado_anterior < 0 < lado_atual:
            return "lado_negativo_para_positivo"

        return "lado_positivo_para_negativo"

    def total_contado(self):
        """Retorna o total de IDs contados."""
        return len(self.ids_contados)
