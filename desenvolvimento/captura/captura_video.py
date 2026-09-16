# Importando bibliotecas json e OpenCV (cv2) para manipulação de arquivos JSON e captura de vídeo.
import json
import cv2

# Definindo o caminho do arquivo JSON que contém as informações das câmeras.
CAMERAS_PATH = "configs/cameras/cameras.json"

# Criando uma função chamada carregar_cameras() que irá ler o arquivo JSON especificado em CAMERAS_PATH e retornar os dados contidos nele.
def carregar_cameras():
    # Abrindo o arquivo JSON no modo de leitura ("r = read") e atribuindo o objeto do arquivo à variável "arquivo". Em seguida, carregando os dados do arquivo JSON usando json.load() e armazenando-os na variável "dados".
    with open(CAMERAS_PATH, "r", encoding="utf-8") as arquivo:
        # Aqui estou pegando o conteúdo do JSON e transformando em uma estrutura de dados do Python (como dicionários e listas) para que possam ser manipulados no código.
        dados = json.load(arquivo)

        # Retornando apenas a lista de câmeras do JSON.
        return dados["cameras"]  # Retornando apenas a lista de câmeras do JSON.

# Criando uma função chamada buscar_cameras() que recebe uma lista de câmeras e um ID de câmera como parâmetros. A função irá procurar na lista de câmeras a câmera que corresponde ao ID fornecido.
def buscar_cameras(cameras, camera_id):
    # Iterando sobre cada câmera na lista de câmeras fornecida.
    for camera in cameras:
        # Verificando se o ID da câmera atual é igual ao ID fornecido como parâmetro. Se for, a função retorna o dicionário da câmera correspondente.
        if camera["id"] == camera_id:
            # Se a câmera com o ID correspondente for encontrada, a função retorna o dicionário da câmera.
            return camera # Retornando o dicionário da câmera correspondente ao ID fornecido.

    # Se nenhuma câmera com o ID correspondente for encontrada, a função retorna None.
    return None

# Criando a função main() que será o ponto de entrada do programa.
def main():
    # Chamando a função carregar_cameras() para obter a lista de câmeras do arquivo JSON.
    cameras = carregar_cameras()

    # Definindo o ID da câmera que será buscada na lista de câmeras. Neste caso, o ID é 36.
    camera_id = 36

    # Chamando a função buscar_cameras() para procurar a câmera com o ID especificado na lista de câmeras carregada. O resultado é armazenado na variável "camera".
    camera = buscar_cameras(cameras, camera_id)

    # Verificando se a câmera com o ID correspondente foi encontrada. Se não for encontrada, uma mensagem de erro será exibida e a função retornará.
    if camera is None:
        # Se a câmera com o ID correspondente for encontrada, a função retorna o dicionário da câmera.
        print(f"Camera com o ID {camera_id} não foi encontrada...")
        return
        capturar_video(camera)  # Chamando a função capturar_video() para iniciar a captura de vídeo da câmera encontrada.

    # Se a câmera com o ID correspondente for encontrada, a função retorna o dicionário da câmera.
    print(f"Camera Selecionada: {camera['nome']}")
    print(f"KM {camera['km']}")
    print(f"Stream: {camera['stream_url']}")

    
    # Criando um objeto de captura de vídeo usando OpenCV (cv2.VideoCapture) com a URL de streaming da câmera e especificando o backend FFMPEG para lidar com o fluxo de vídeo.
    captura = cv2.VideoCapture(
        camera["stream_url"],
        cv2.CAP_FFMPEG
    )

    # aqui estou verificando se a captura de vídeo foi aberta com sucesso. Se não for possível abrir a captura, uma mensagem de erro será exibida e a função retornará.
    print(f"backend utilizado: {captura.getBackendName()}")

    # Verificando se a captura de vídeo foi aberta com sucesso. Se não for possível abrir a captura, uma mensagem de erro será exibida e a função retornará.
    if not captura.isOpened():
        print("Erro ao abrir a captura de vídeo.")
        return

    # Se a captura de vídeo foi aberta com sucesso, uma mensagem de sucesso será exibida, indicando que a captura de vídeo foi iniciada para a câmera selecionada.
    print(f"Captura de vídeo iniciada com sucesso para a câmera {camera['nome']}.")
    print("Pressione 'esc' para sair.")

    # Iniciando um loop infinito para capturar e exibir os frames do vídeo em tempo real.
    while True:

        # Lendo um frame da captura de vídeo. A variável "sucesso" indica se a leitura foi bem-sucedida, e "frame" contém o frame capturado.
        sucesso, frame = captura.read()

        # Verificando se a leitura do frame foi bem-sucedida. Se não for possível capturar o frame, uma mensagem de erro será exibida e o loop será interrompido.
        if not sucesso:
            print("Erro ao capturar o frame de vídeo.")
            break

        # Exibindo o frame capturado em uma janela chamada "Captura de Vídeo". A função cv2.imshow() é usada para mostrar o frame na tela.
        print(f"Frame capturado: {frame.shape}")

        # Exibindo o frame capturado em uma janela chamada "RoadVision - Captura de Vídeo". A função cv2.imshow() é usada para mostrar o frame na tela.
        cv2.imshow("RoadVision - Captura de Vídeo", frame)

        # A função cv2.waitKey() é usada para aguardar por uma tecla ser pressionada. O valor retornado é armazenado na variável "tecla". O operador bitwise AND (&) é usado para garantir que apenas os 8 bits menos significativos sejam considerados.
        tecla = cv2.waitKey(100) & 0xFF

        # Verificando se a tecla 'esc' foi pressionada (código ASCII 27). Se for, uma mensagem de saída será exibida e o loop será interrompido.
        if tecla == 27:  # Verificando se a tecla 'esc' foi pressionada (código ASCII 27).
            print("Saindo da captura de vídeo...")
            break

    # Após sair do loop, liberando os recursos da captura de vídeo e fechando todas as janelas abertas pelo OpenCV.
            captura.release()  # Liberando os recursos da captura de vídeo.
            cv2.destroyAllWindows()  # Fechando todas as janelas abertas pelo OpenCV.

        
# Chamando a função main() apenas se o script for executado diretamente (não importado como módulo). Isso garante que a função main() seja executada apenas quando o script for o ponto de entrada do programa.
if __name__ == "__main__":
    main()