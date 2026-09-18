import cv2
import time


MAX_TENTATIVAS = 3
TEMPO_ESPERA = 5


def verificar_conexao(captura):
    if not captura.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return False

    return True


def tratar_falha_conexao():
    print("Não foi possível conectar com a câmera.")
    print(
        f"Aguardando {TEMPO_ESPERA} segundos "
        "antes de tentar novamente..."
    )

    time.sleep(TEMPO_ESPERA)


def tentar_reconectar(camera):
    print("Tentando reconectar à câmera...")

    captura = cv2.VideoCapture(
        camera["stream_url"],
        cv2.CAP_FFMPEG
    )

    if verificar_conexao(captura):
        print("Reconexão bem-sucedida!")
        return captura

    captura.release()

    return None


def tratar_indisponibilidade(camera):
    print(
        f"A câmera {camera['nome']} "
        f"permanece indisponível após "
        f"{MAX_TENTATIVAS} tentativas de reconexão."
    )


def executar_reconexao(camera):
    for tentativa in range(1, MAX_TENTATIVAS + 1):

        print(
            f"Tentativa de reconexão "
            f"{tentativa} de {MAX_TENTATIVAS} "
            f"para a câmera {camera['nome']}..."
        )

        captura = tentar_reconectar(camera)

        if captura is not None:
            return captura

        if tentativa < MAX_TENTATIVAS:
            tratar_falha_conexao()

    tratar_indisponibilidade(camera)

    return None


if __name__ == "__main__":

    camera_teste = {
        "id": 36,
        "nome": "KM 055+000 - Maranduba",
        "stream_url": "http://200.144.30.103:8084/hls/cam_36/stream.m3u8"
    }

    executar_reconexao(camera_teste)