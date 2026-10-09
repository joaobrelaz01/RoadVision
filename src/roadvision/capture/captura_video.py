# Importando bibliotecas json e OpenCV (cv2) para manipulação de arquivos JSON e captura de vídeo.
import json
import cv2
from pathlib import Path

from roadvision.detection.detector_yolo import YOLODetector
from roadvision.capture.extracao_frames import ExtratorFrames
from roadvision.capture.tratamento_falha_camera import executar_reconexao


# Definindo o caminho do arquivo JSON que contém as informações das câmeras.
CAMERAS_PATH = (
    Path(__file__).resolve().parents[3]
    / "configs"
    / "cameras"
    / "cameras.json"
)


# Criando uma função chamada carregar_cameras() que irá ler o arquivo JSON.
def carregar_cameras():
    with open(CAMERAS_PATH, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados["cameras"]


# Criando uma função para buscar uma câmera pelo ID.
def buscar_cameras(cameras, camera_id):
    for camera in cameras:
        if camera["id"] == camera_id:
            return camera

    return None


# Criando a função main(), ponto de entrada do programa.
def main():

    # Carregando as câmeras do arquivo JSON.
    cameras = carregar_cameras()

    # Carregando o modelo YOLO.
    print("Carregando detector YOLO...")
    detector = YOLODetector()

    # Definindo o ID da câmera.
    camera_id = 36

    # Buscando a câmera.
    camera = buscar_cameras(cameras, camera_id)

    if camera is None:
        print(f"Camera com o ID {camera_id} não foi encontrada...")
        return

    print(f"Camera Selecionada: {camera['nome']}")
    print(f"KM {camera['km']}")
    print(f"Stream: {camera['stream_url']}")

    # Abrindo o stream da câmera.
    captura = cv2.VideoCapture(
        camera["stream_url"],
        cv2.CAP_FFMPEG
    )

    if not captura.isOpened():
        print("Erro ao abrir a captura de vídeo.")
        return

    print(f"Backend utilizado: {captura.getBackendName()}")

    print(
        f"Captura de vídeo iniciada com sucesso "
        f"para a câmera {camera['nome']}."
    )

    print("Pressione 'ESC' para sair.")

    # Configurando a extração de frames.
    extrator = ExtratorFrames(intervalo_segundos=2.0)

    # Loop de captura dos frames.
    while True:

        sucesso, frame = captura.read()

        if not sucesso:
            print("Erro ao capturar o frame de vídeo.")
            captura.release()

            captura = executar_reconexao(camera)

            if captura is None:
                print("Encerrando a captura após falha de reconexão.")
                break

            print("Captura de vídeo restaurada com sucesso.")
            continue

        # Enviando o frame para o extrator.
        frame_extraido = extrator.processar(frame)

        # Quando um frame é extraído, ele é enviado para o YOLO.
        if frame_extraido is not None:

            # Executando a detecção de veículos.
            resultado = detector.detect(frame_extraido)

            # Resultado do YOLO processado sem interface gráfica.
            quantidade_deteccoes = len(resultado.boxes)

            print(
                f"Detecções encontradas: {quantidade_deteccoes}"
            )

    # Liberando os recursos.
    captura.release()


# Executando o programa somente quando o arquivo for executado diretamente.
if __name__ == "__main__":
    main()