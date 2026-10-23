
"""Utilitários para filtrar veículos pela região de interesse (ROI)."""

import json
from pathlib import Path

import cv2
import numpy as np


REGIOES_PATH = (
    Path(__file__).resolve().parents[2]
    / "configs"
    / "cameras"
    / "regioes.json"
)


def carregar_regiao(camera_id):
    """Carrega os pontos normalizados de uma câmera."""
    with open(REGIOES_PATH, "r", encoding="utf-8-sig") as arquivo:
        configuracao = json.load(arquivo)

    regiao = configuracao["cameras"].get(str(camera_id))

    if regiao is None:
        raise ValueError(
            f"Não existe região configurada para a câmera {camera_id}."
        )

    pontos = np.array(
        regiao["pontos_normalizados"],
        dtype=np.float32,
    )

    if len(pontos) < 3:
        raise ValueError("A região precisa ter pelo menos 3 pontos.")

    if (
        not np.isfinite(pontos).all()
        or np.any(pontos < 0)
        or np.any(pontos > 1)
    ):
        raise ValueError(
            "Os pontos normalizados devem estar entre 0 e 1."
        )

    return pontos


def converter_para_pixels(pontos_normalizados, largura, altura):
    """Converte pontos normalizados para coordenadas da imagem."""
    pontos = pontos_normalizados.copy()
    pontos[:, 0] *= largura - 1
    pontos[:, 1] *= altura - 1

    return np.round(pontos).astype(np.int32)


def ponto_dentro_da_regiao(ponto, poligono):
    """Verifica se um ponto está dentro ou sobre o polígono."""
    return cv2.pointPolygonTest(
        poligono,
        (float(ponto[0]), float(ponto[1])),
        False,
    ) >= 0


def obter_ids_dentro_da_regiao(resultado, poligono):
    """Retorna IDs cujos pontos inferiores centrais estão na ROI."""
    boxes = resultado.boxes

    if boxes is None or boxes.id is None:
        return set()

    ids = boxes.id.int().cpu().tolist()
    caixas = boxes.xyxy.cpu().tolist()

    ids_validos = set()

    for track_id, caixa in zip(ids, caixas):
        x1, y1, x2, y2 = caixa

        # Aproxima o ponto de contato do veículo com o solo.
        ponto = ((x1 + x2) / 2, y2)

        if ponto_dentro_da_regiao(ponto, poligono):
            ids_validos.add(track_id)

    return ids_validos


def desenhar_regiao(frame, poligono):
    """Desenha o limite da ROI para conferência visual."""
    overlay = frame.copy()

    cv2.fillPoly(overlay, [poligono], (0, 180, 0))
    cv2.addWeighted(overlay, 0.12, frame, 0.88, 0, frame)

    cv2.polylines(
        frame,
        [poligono],
        isClosed=True,
        color=(0, 255, 255),
        thickness=2,
    )

    return frame