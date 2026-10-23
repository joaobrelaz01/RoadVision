
from collections import defaultdict, deque
from math import hypot


CLASSES_VEICULOS = {
    2: "carro",
    3: "moto",
    5: "onibus",
    7: "caminhao",
}


class VehicleTracker:
    """Rastreia veículos, suas categorias e estados de movimento."""

    def __init__(
        self,
        model,
        history_length=30,
        janela_movimento=10,
        limite_parado=8.0,
        limite_lento=25.0,
        frames_confirmacao=5,
        limite_inatividade=300,
        intervalo_limpeza=30,
    ):
        if history_length < 1:
            raise ValueError("history_length deve ser maior que zero.")
        if janela_movimento < 2:
            raise ValueError("janela_movimento deve ser pelo menos 2.")
        if not 0 <= limite_parado < limite_lento:
            raise ValueError("Os limites de movimento são inválidos.")
        if frames_confirmacao < 1:
            raise ValueError("frames_confirmacao deve ser maior que zero.")
        if limite_inatividade < 1:
            raise ValueError("limite_inatividade deve ser maior que zero.")
        if intervalo_limpeza < 1:
            raise ValueError("intervalo_limpeza deve ser maior que zero.")

        self.model = model

        tamanho_historico = max(
            history_length,
            janela_movimento + 1,
        )
        self.history = defaultdict(
            lambda: deque(maxlen=tamanho_historico)
        )

        # IDs distintos observados durante esta execução.
        self.unique_ids = set()

        # Associação entre cada ID rastreado e sua categoria.
        self.vehicle_classes = {}

        self.active_ids = []
        self.states = {}
        self.pending_states = {}
        self.state_streaks = defaultdict(int)

        self.janela_movimento = janela_movimento
        self.limite_parado = limite_parado
        self.limite_lento = limite_lento
        self.frames_confirmacao = frames_confirmacao

        self.limite_inatividade = limite_inatividade
        self.intervalo_limpeza = intervalo_limpeza
        self.frame_index = 0
        self.last_seen = {}
        self.frames_desde_limpeza = 0

    def track(self, frame):
        """Rastreia veículos, atualiza estados e limpa dados antigos."""
        resultados = self.model.track(
            frame,
            persist=True,
            classes=list(CLASSES_VEICULOS.keys()),
            tracker="bytetrack.yaml",
            verbose=False,
        )

        resultado = resultados[0]

        self.frame_index += 1
        self.frames_desde_limpeza += 1
        self.active_ids = []

        boxes = resultado.boxes

        if boxes is not None and boxes.id is not None:
            ids = boxes.id.int().cpu().tolist()
            caixas = boxes.xyxy.cpu().tolist()
            classes = boxes.cls.int().cpu().tolist()

            for track_id, caixa, classe_id in zip(
                ids, caixas, classes
            ):
                tipo_veiculo = CLASSES_VEICULOS.get(classe_id)

                # Ignora classes que não pertencem às categorias suportadas.
                if tipo_veiculo is None:
                    continue

                x1, y1, x2, y2 = map(int, caixa)
                centro = (
                    (x1 + x2) // 2,
                    (y1 + y2) // 2,
                )

                self.vehicle_classes[track_id] = tipo_veiculo
                self.history[track_id].append(centro)
                self.unique_ids.add(track_id)
                self.active_ids.append(track_id)
                self.last_seen[track_id] = self.frame_index

                estado_estimado = self._estimar_estado(track_id)
                estado_atual = self.states.get(track_id)

                if estado_atual is None:
                    self.states[track_id] = estado_estimado
                    self.pending_states.pop(track_id, None)
                    self.state_streaks[track_id] = 0

                elif estado_estimado == estado_atual:
                    self.pending_states.pop(track_id, None)
                    self.state_streaks[track_id] = 0

                else:
                    if (
                        self.pending_states.get(track_id)
                        == estado_estimado
                    ):
                        self.state_streaks[track_id] += 1
                    else:
                        self.pending_states[track_id] = estado_estimado
                        self.state_streaks[track_id] = 1

                    if (
                        self.state_streaks[track_id]
                        >= self.frames_confirmacao
                    ):
                        self.states[track_id] = estado_estimado
                        self.pending_states.pop(track_id, None)
                        self.state_streaks[track_id] = 0

        if self.frames_desde_limpeza >= self.intervalo_limpeza:
            self.limpar_inativos()
            self.frames_desde_limpeza = 0

        return resultado

    def limpar_inativos(self):
        """Remove trajetórias e estados de IDs inativos por tempo excessivo."""
        inativos = [
            track_id
            for track_id, ultimo_frame in self.last_seen.items()
            if (
                self.frame_index - ultimo_frame
                >= self.limite_inatividade
            )
        ]

        for track_id in inativos:
            self.history.pop(track_id, None)
            self.states.pop(track_id, None)
            self.pending_states.pop(track_id, None)
            self.state_streaks.pop(track_id, None)
            self.last_seen.pop(track_id, None)
            self.vehicle_classes.pop(track_id, None)

        return len(inativos)

    def _estimar_estado(self, track_id):
        """Estima o movimento pelo deslocamento da trajetória."""
        pontos = list(self.history[track_id])

        if len(pontos) < self.janela_movimento + 1:
            return "INDEFINIDO"

        inicio = pontos[-(self.janela_movimento + 1)]
        fim = pontos[-1]

        deslocamento = hypot(
            fim[0] - inicio[0],
            fim[1] - inicio[1],
        )

        if deslocamento <= self.limite_parado:
            return "PARADO"

        if deslocamento <= self.limite_lento:
            return "LENTO"

        return "MOVENDO"

    def get_trajectory(self, track_id):
        """Retorna as posições registradas de um veículo."""
        return list(self.history.get(track_id, []))

    def get_active_ids(self):
        """Retorna os IDs encontrados no frame mais recente."""
        return self.active_ids.copy()

    def get_unique_count(self):
        """Retorna a quantidade de IDs distintos nesta execução."""
        return len(self.unique_ids)

    def get_vehicle_state(self, track_id):
        """Retorna o estado confirmado de um veículo."""
        return self.states.get(track_id, "INDEFINIDO")

    def get_active_states(self):
        """Retorna os estados dos veículos do frame atual."""
        return {
            track_id: self.get_vehicle_state(track_id)
            for track_id in self.active_ids
        }

    def get_vehicle_type(self, track_id):
        """Retorna a categoria associada ao ID rastreado."""
        return self.vehicle_classes.get(track_id)
