
"""Executa a primeira detecção de veículos em imagens locais usando YOLO."""

import argparse
from pathlib import Path

import cv2

from roadvision.detection.detector_yolo import YOLODetector


RAIZ_PROJETO = Path(__file__).resolve().parents[3]
PASTA_DADOS = RAIZ_PROJETO / "data"
PASTA_RESULTADOS = PASTA_DADOS / "resultados"

# Classes COCO: carro = 2, moto = 3, caminhão = 7.
CLASSES_ALVO = {
    2: "carro",
    3: "moto",
    7: "caminhao",
}

EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def encontrar_imagens(caminho=None):
    """Localiza uma imagem específica ou imagens dentro de data/."""
    if caminho:
        arquivo = Path(caminho)
        if not arquivo.is_absolute():
            arquivo = RAIZ_PROJETO / arquivo

        if not arquivo.is_file():
            raise FileNotFoundError(f"Imagem não encontrada: {arquivo}")

        return [arquivo]

    imagens = [
        arquivo
        for arquivo in PASTA_DADOS.rglob("*")
        if arquivo.is_file()
        and arquivo.suffix.lower() in EXTENSOES_IMAGEM
        and PASTA_RESULTADOS not in arquivo.parents
    ]

    if not imagens:
        raise FileNotFoundError(
            f"Nenhuma imagem encontrada em {PASTA_DADOS}.\n"
            "Coloque uma imagem de veículos em data/ e tente novamente."
        )

    return imagens


def executar_deteccao(caminho_imagem, detector):
    """Detecta veículos, exibe as classes encontradas e salva a imagem."""
    imagem = cv2.imread(str(caminho_imagem))

    if imagem is None:
        print(f"Não foi possível abrir a imagem: {caminho_imagem}")
        return False

    # Usa o modelo já carregado pelo YOLODetector.
    resultado = detector.model.predict(
        imagem,
        classes=list(CLASSES_ALVO.keys()),
        verbose=False,
    )[0]

    print(f"\nImagem: {caminho_imagem.name}")
    print(f"Veículos detectados: {len(resultado.boxes)}")

    for caixa in resultado.boxes:
        classe_id = int(caixa.cls[0].item())
        confianca = float(caixa.conf[0].item())
        x1, y1, x2, y2 = map(int, caixa.xyxy[0].tolist())

        print(
            f"- {CLASSES_ALVO[classe_id]} | "
            f"confiança: {confianca:.2%} | "
            f"caixa: ({x1}, {y1}, {x2}, {y2})"
        )

    imagem_anotada = resultado.plot()
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    destino = PASTA_RESULTADOS / f"{caminho_imagem.stem}_deteccao.jpg"

    if not cv2.imwrite(str(destino), imagem_anotada):
        print(f"Erro ao salvar o resultado: {destino}")
        return False

    print(f"Resultado salvo em: {destino}")

    # Exibe a imagem anotada em uma janela.
    cv2.imshow("RoadVision - Deteccao YOLO", imagem_anotada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Detecta carros, motos e caminhões em imagens usando YOLO."
    )
    parser.add_argument(
        "imagem",
        nargs="?",
        help="Caminho da imagem. Se omitido, procura imagens em data/.",
    )
    args = parser.parse_args()

    try:
        imagens = encontrar_imagens(args.imagem)

        print("Carregando modelo YOLO...")
        detector = YOLODetector()
        print(f"Modelo carregado: {detector.model_path}")

        sucessos = 0
        for imagem in imagens:
            if executar_deteccao(imagem, detector):
                sucessos += 1

        print(f"\nConcluído: {sucessos}/{len(imagens)} imagem(ns) processada(s).")

    except (FileNotFoundError, RuntimeError, OSError) as erro:
        print(f"Erro: {erro}")
        raise SystemExit(1) from erro


if __name__ == "__main__":
    main()
