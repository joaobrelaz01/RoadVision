# Importando bibliotecas json e OpenCV (cv2) para manipulação de arquivos JSON e captura de vídeo.
import json
import cv2
from pathlib import Path

<<<<<<< HEAD
from roadvision.detection.detector_yolo import YOLODetector


# Definindo o caminho do arquivo JSON que contém as informações das câmeras.
CAMERAS_PATH = (
    Path(__file__).resolve().parents[3]
    / "configs"
    / "cameras"
    / "cameras.json"
)


# Criando uma função chamada carregar_cameras() que irá ler o arquivo JSON.
=======
# NOVA IMPORTAÇÃO: Trazendo o nosso extrator de frames
from extracao_frames import ExtratorFrames

# Definindo o caminho do arquivo JSON que contém as informações das câmeras.
CAMERAS_PATH = Path(__file__).resolve().parents[3] / "configs" / "cameras" / "cameras.json"

>>>>>>> origin/main
def carregar_cameras():
    with open(CAMERAS_PATH, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados["cameras"] 

<<<<<<< HEAD
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
=======
def buscar_cameras(cameras, camera_id):
    for camera in cameras:
        if camera["id"] == camera_id:
            return camera 
    return None

def main():
    cameras = carregar_cameras()
    camera_id = 36
>>>>>>> origin/main
    camera = buscar_cameras(cameras, camera_id)

    if camera is None:
        print(f"Camera com o ID {camera_id} não foi encontrada...")
        return

    print(f"Camera Selecionada: {camera['nome']}")
    print(f"KM {camera['km']}")
    print(f"Stream: {camera['stream_url']}")

<<<<<<< HEAD
    # Abrindo o stream da câmera.
=======
>>>>>>> origin/main
    captura = cv2.VideoCapture(
        camera["stream_url"],
        cv2.CAP_FFMPEG
    )

<<<<<<< HEAD
    print(f"Backend utilizado: {captura.getBackendName()}")
=======
    print(f"backend utilizado: {captura.getBackendName()}")
>>>>>>> origin/main

    if not captura.isOpened():
        print("Erro ao abrir a captura de vídeo.")
        return

<<<<<<< HEAD
    print(
        f"Captura de vídeo iniciada com sucesso "
        f"para a câmera {camera['nome']}."
    )

    print("Pressione 'ESC' para sair.")

    # Loop de captura dos frames.
    while True:

        # Capturando um frame.
=======
    print(f"Captura de vídeo iniciada com sucesso para a câmera {camera['nome']}.")
    print("Pressione 'esc' para sair.")

    # NOVA CONFIGURAÇÃO: Definindo o intervalo para extrair 1 frame a cada 2.0 segundos
    extrator = ExtratorFrames(intervalo_segundos=2.0)

    while True:
>>>>>>> origin/main
        sucesso, frame = captura.read()

        if not sucesso:
            print("Erro ao capturar o frame de vídeo.")
            break

<<<<<<< HEAD
        # Enviando o frame para o detector YOLO.
        resultado = detector.detect(frame)

        # Desenhando as detecções encontradas pelo YOLO.
        frame_analisado = resultado.plot()

        # Mostrando o frame com as detecções.
        cv2.imshow(
            "RoadVision - Captura de Video + YOLO",
            frame_analisado
        )

        # Verificando se ESC foi pressionado.
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == 27:
            print("Saindo da captura de vídeo...")
            break

    # Liberando os recursos.
    captura.release()
    cv2.destroyAllWindows()


# Executando o programa somente quando o arquivo for executado diretamente.
=======
        # NOVA LÓGICA: Passando o frame da câmera para o extrator avaliar
        frame_extraido = extrator.processar(frame)
        
        # Se o extrator devolveu um frame, significa que deu o tempo certo (2 segundos)
        if frame_extraido is not None:
            print(f"✅ Frame extraído com sucesso para IA! Tamanho: {frame_extraido.shape}")

        cv2.imshow("RoadVision - Captura de Vídeo", frame)

        tecla = cv2.waitKey(100) & 0xFF

        if tecla == 27:  
            print("Saindo da captura de vídeo...")
            break

    captura.release() 
    cv2.destroyAllWindows() 

>>>>>>> origin/main
if __name__ == "__main__":
    main()