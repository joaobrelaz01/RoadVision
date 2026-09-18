# Estou importando a biblioteca json para manipulação de arquivos JSON e a biblioteca OpenCV (cv2) para captura e processamento de vídeo.
import json
import cv2
from pathlib import Path

# Estou criando uma função chamada carregar_cameras() que irá ler um arquivo JSON chamado "cameras.json" e retornar os dados contidos nele.
def carregar_cameras():
# Estou abrindo o arquivo "cameras.json" no modo de leitura ("r = read") e atribuindo o objeto do arquivo à variável "arquivo". Em seguida, estou carregando os dados do arquivo JSON usando json.load() e armazenando-os na variável "dados".
    cameras_path = Path(__file__).resolve().parents[3] / "configs" / "cameras" / "cameras.json"
    with open(cameras_path, "r", encoding="utf-8") as arquivo:
# Aqui estou pegando o conteudo do json e transforma em estrutura de dados do Python (como dicionários e listas) para que possam ser manipulados no código.
            dados = json.load(arquivo)

# Estou retornando os dados carregados do arquivo JSON para que possam ser utilizados em outras partes do código.
    return dados

def main():
      cameras = carregar_cameras()

      print(cameras)


if __name__ == "__main__":
    main()


