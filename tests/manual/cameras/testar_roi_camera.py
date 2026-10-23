import json
from pathlib import Path

import cv2
import numpy as np

CAMERAS_PATH = (
    Path(__file__).resolve().parents[3]
    / "configs"
    / "cameras"
    / "cameras.json"
)

REGIOES_PATH = CAMERAS_PATH.parent / "regioes.json"

CAMERA_ID = 36

pontos = []


def carregar_camera():
    with open(CAMERAS_PATH, "r", encoding="utf-8-sig") as arquivo:
        cameras = json.load(arquivo)["cameras"]

    for camera in cameras:
        if camera["id"] == CAMERA_ID:
            return camera

    raise ValueError(f"Câmera {CAMERA_ID} não encontrada.")


def clique_mouse(evento, x, y, flags, frame):
    if evento == cv2.EVENT_LBUTTONDOWN:
        pontos.append((x, y))
    elif evento == cv2.EVENT_RBUTTONDOWN and pontos:
        pontos.pop()


def desenhar(frame):
    visualizacao = frame.copy()

    for ponto in pontos:
        cv2.circle(visualizacao, ponto, 5, (0, 0, 255), -1)

    if len(pontos) >= 2:
        cv2.polylines(
            visualizacao,
            [np.array(pontos, dtype=np.int32)],
            False,
            (0, 255, 255),
            2,
        )

    if len(pontos) >= 3:
        overlay = visualizacao.copy()
        cv2.fillPoly(
            overlay,
            [np.array(pontos, dtype=np.int32)],
            (0, 180, 0),
        )
        visualizacao = cv2.addWeighted(
            overlay, 0.18, visualizacao, 0.82, 0
        )

        # Redesenha os limites para ficarem visíveis.
        cv2.polylines(
            visualizacao,
            [np.array(pontos, dtype=np.int32)],
            False,
            (0, 255, 255),
            2,
        )

    instrucoes = [
        "Clique esquerdo: adicionar ponto",
        "Clique direito: desfazer ultimo ponto",
        "S: salvar | C: limpar | ESC: sair",
        f"Camera {CAMERA_ID} | Pontos: {len(pontos)}",
    ]

    for indice, texto in enumerate(instrucoes):
        cv2.putText(
            visualizacao,
            texto,
            (10, 25 + indice * 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

    return visualizacao


def salvar_regiao(largura, altura):
    if len(pontos) < 3:
        print("Marque pelo menos 3 pontos antes de salvar.")
        return

    poligono = np.array(pontos, dtype=np.float32)

    # Normaliza para permitir resoluções diferentes.
    poligono[:, 0] /= largura - 1
    poligono[:, 1] /= altura - 1

    if not REGIOES_PATH.exists():
        configuracao = {"cameras": {}}
    else:
        with open(
            REGIOES_PATH, "r", encoding="utf-8-sig"
        ) as arquivo:
            configuracao = json.load(arquivo)

    configuracao.setdefault("cameras", {})[str(CAMERA_ID)] = {
        "pontos_normalizados": poligono.tolist()
    }

    REGIOES_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REGIOES_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(
            configuracao,
            arquivo,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Região da câmera {CAMERA_ID} salva em {REGIOES_PATH}")


def main():
    camera = carregar_camera()
    captura = cv2.VideoCapture(
        camera["stream_url"], cv2.CAP_FFMPEG
    )

    try:
        if not captura.isOpened():
            print("Não foi possível abrir a câmera.")
            return

        nome_janela = "RoadVision - Configurar ROI"
        cv2.namedWindow(nome_janela)
        cv2.setMouseCallback(nome_janela, clique_mouse)

        print("Clique nos cantos da região que deseja incluir.")
        print("S para salvar | C para limpar | ESC para sair.")

        while True:
            sucesso, frame = captura.read()

            if not sucesso:
                print("Falha ao receber frame da câmera.")
                break

            altura, largura = frame.shape[:2]
            cv2.imshow(nome_janela, desenhar(frame))

            tecla = cv2.waitKey(1) & 0xFF

            if tecla == 27:
                break
            elif tecla in (ord("c"), ord("C")):
                pontos.clear()
                print("Pontos removidos.")
            elif tecla in (ord("s"), ord("S")):
                salvar_regiao(largura, altura)

    finally:
        captura.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
