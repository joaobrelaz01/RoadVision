
import argparse
import json
import time
from pathlib import Path

import cv2

from roadvision.detection.detector_yolo import YOLODetector


ROOT_DIR = Path(__file__).resolve().parents[3]
VIDEO_DEFAULT = ROOT_DIR / "data" / "videos" / "der_cam_14.mp4"
OUTPUT_DEFAULT = ROOT_DIR / "data" / "resultados" / "detection"


def avaliar_video(video_path, output_dir, intervalo_segundos=2.0):
    video_path = Path(video_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not video_path.is_file():
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    imagens_dir = output_dir / "amostras"
    imagens_dir.mkdir(parents=True, exist_ok=True)

    detector = YOLODetector()
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Não foi possível abrir: {video_path}")

    fps_video = cap.get(cv2.CAP_PROP_FPS)
    if fps_video <= 0:
        fps_video = 20.0

    passo = max(1, int(fps_video * intervalo_segundos))
    frame_atual = 0
    amostras = []
    inicio = time.perf_counter()

    try:
        while True:
            sucesso, frame = cap.read()
            if not sucesso:
                break

            if frame_atual % passo == 0:
                resultado = detector.detect(frame)

                deteccoes = []
                boxes = resultado.boxes

                if boxes is not None:
                    for box in boxes:
                        classe_id = int(box.cls[0].item())
                        confianca = float(box.conf[0].item())
                        x1, y1, x2, y2 = (
                            int(valor)
                            for valor in box.xyxy[0].tolist()
                        )

                        deteccoes.append({
                            "classe_id": classe_id,
                            "classe": detector.CLASSES_VEICULOS.get(
                                classe_id, f"classe_{classe_id}"
                            ),
                            "confianca": round(confianca, 4),
                            "caixa_xyxy": [x1, y1, x2, y2],
                            "revisao_manual": {
                                "veiculo_real": None,
                                "classe_correta": None,
                                "observacao": ""
                            }
                        })

                nome_imagem = f"frame_{frame_atual:06d}.jpg"
                caminho_imagem = imagens_dir / nome_imagem
                imagem_anotada = resultado.plot()

                if not cv2.imwrite(
                    str(caminho_imagem), imagem_anotada
                ):
                    raise RuntimeError(
                        f"Não foi possível salvar {caminho_imagem}"
                    )

                amostras.append({
                    "frame": frame_atual,
                    "tempo_segundos": round(frame_atual / fps_video, 2),
                    "imagem": str(caminho_imagem),
                    "total_deteccoes": len(deteccoes),
                    "deteccoes": deteccoes,
                    "revisao_manual": {
                        "veiculos_reais_na_imagem": None,
                        "veiculos_nao_detectados": None,
                        "falsos_positivos": None,
                        "classificacoes_incorretas": None,
                        "objetos_estaticos_detectados": None,
                        "observacoes": ""
                    }
                })

                print(
                    f"Amostra: frame {frame_atual} | "
                    f"detecções: {len(deteccoes)}"
                )

            frame_atual += 1

    finally:
        cap.release()

    relatorio = {
        "video": str(video_path),
        "modelo": str(detector.model_path),
        "fps_video": round(fps_video, 2),
        "intervalo_amostras_segundos": intervalo_segundos,
        "frames_lidos": frame_atual,
        "total_amostras": len(amostras),
        "tempo_execucao_segundos": round(
            time.perf_counter() - inicio, 2
        ),
        "status_avaliacao": "PENDENTE_REVISAO_MANUAL",
        "observacao": (
            "As métricas de precisão e recall não são calculadas "
            "automaticamente. Preencha a revisão manual comparando "
            "cada amostra com os veículos realmente visíveis."
        ),
        "amostras": amostras
    }

    caminho_json = output_dir / "avaliacao_precisao.json"
    with caminho_json.open("w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)

    print("\n===== AVALIAÇÃO GERADA =====")
    print(f"Frames lidos: {frame_atual}")
    print(f"Amostras salvas: {len(amostras)}")
    print(f"Relatório JSON: {caminho_json}")
    print("A revisão manual ainda é necessária.")


def main():
    parser = argparse.ArgumentParser(
        description="Gera amostras para avaliar a precisão do YOLO."
    )
    parser.add_argument(
        "--video", default=str(VIDEO_DEFAULT)
    )
    parser.add_argument(
        "--output-dir", default=str(OUTPUT_DEFAULT)
    )
    parser.add_argument(
        "--intervalo", type=float, default=2.0,
        help="Intervalo entre amostras, em segundos."
    )
    args = parser.parse_args()

    if args.intervalo <= 0:
        parser.error("--intervalo precisa ser maior que zero.")

    avaliar_video(args.video, args.output_dir, args.intervalo)


if __name__ == "__main__":
    main()
