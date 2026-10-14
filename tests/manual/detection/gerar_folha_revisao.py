
from pathlib import Path
import math

import cv2
import numpy as np


ROOT_DIR = Path(__file__).resolve().parents[3]
PASTA_IMAGENS = (
    ROOT_DIR / "data" / "resultados" / "detection" / "amostras"
)
ARQUIVO_SAIDA = (
    ROOT_DIR / "data" / "resultados" / "detection"
    / "folha_revisao.jpg"
)

LARGURA_MINIATURA = 240
ALTURA_MINIATURA = 180
ALTURA_TITULO = 28
COLUNAS = 4


def main():
    arquivos = sorted(PASTA_IMAGENS.glob("frame_*.jpg"))

    if not arquivos:
        raise FileNotFoundError(
            f"Nenhuma amostra encontrada em {PASTA_IMAGENS}"
        )

    miniaturas = []

    for arquivo in arquivos:
        imagem = cv2.imread(str(arquivo))

        if imagem is None:
            print(f"Aviso: não foi possível abrir {arquivo.name}")
            continue

        miniatura = cv2.resize(
            imagem,
            (LARGURA_MINIATURA, ALTURA_MINIATURA),
        )

        titulo = arquivo.stem.replace("frame_", "Frame ")
        faixa = np.full(
            (ALTURA_TITULO, LARGURA_MINIATURA, 3),
            255,
            dtype=np.uint8,
        )

        cv2.putText(
            faixa,
            titulo,
            (8, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

        miniaturas.append(np.vstack([faixa, miniatura]))

    if not miniaturas:
        raise RuntimeError("Nenhuma imagem válida para a folha.")

    linhas = math.ceil(len(miniaturas) / COLUNAS)
    largura_celula = LARGURA_MINIATURA
    altura_celula = ALTURA_MINIATURA + ALTURA_TITULO

    folha = np.full(
        (linhas * altura_celula, COLUNAS * largura_celula, 3),
        225,
        dtype=np.uint8,
    )

    for indice, miniatura in enumerate(miniaturas):
        linha = indice // COLUNAS
        coluna = indice % COLUNAS

        y = linha * altura_celula
        x = coluna * largura_celula

        folha[
            y:y + altura_celula,
            x:x + largura_celula,
        ] = miniatura

    ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(ARQUIVO_SAIDA), folha):
        raise RuntimeError("Não foi possível salvar a folha.")

    print(f"Amostras incluídas: {len(miniaturas)}")
    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()
