import time
import numpy as np

class ExtratorFrames:
    def __init__(self, intervalo_segundos: float = 1.0):
        """
        Inicializa o extrator de frames.
        :param intervalo_segundos: Frequência de extração (ex: 1.0 = 1 frame por segundo).
        """
        self.intervalo_segundos = intervalo_segundos
        self.ultimo_tempo_extracao = 0.0

    def deve_extrair(self) -> bool:
        """Verifica se já passou o tempo necessário desde a última extração."""
        tempo_atual = time.time()
        if (tempo_atual - self.ultimo_tempo_extracao) >= self.intervalo_segundos:
            self.ultimo_tempo_extracao = tempo_atual
            return True
        return False

    def processar(self, frame: np.ndarray):
        """
        Recebe o frame da câmera. Se estiver no intervalo correto, retorna a imagem.
        Caso contrário, retorna None.
        """
        if frame is not None and self.deve_extrair():
            return frame
        return None