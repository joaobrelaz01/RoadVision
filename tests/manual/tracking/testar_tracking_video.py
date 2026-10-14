
import argparse
import json
import time
from collections import Counter
from pathlib import Path

import cv2
from ultralytics import YOLO

from roadvision.tracking import CLASSES_VEICULOS, VehicleTracker


ROOT_DIR = Path(__file__).resolve().parents[3]
MODEL_DEFAULT = ROOT_DIR / "models" / "yolo11n.pt"
OUTPUT_DEFAULT = ROOT_DIR / "data" / "resultados" / "tracking"


def processar_video(video_path, model_path, output_dir, exibir=False):
    video_path = Path(video_path).resolve()
    model_path = Path(model_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not video_path.is_file():
        raise FileNotFoundError(f"Video nao encontrado: {video_path}")

    if not model_path.is_file():
        raise FileNotFoundError(f"Modelo YOLO nao encontrado: {model_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    nome = video_path.stem
    video_saida = output_dir / f"{nome}_tracking.mp4"
    relatorio_saida = output_dir / f"{nome}_relatorio.json"

    print(f"Video de entrada: {video_path}")
    print(f"Modelo: {model_path}")
    print("Carregando YOLO...")

    model = YOLO(str(model_path))
    tracker = VehicleTracker(model)

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Nao foi possivel abrir o video: {video_path}")

    fps_video = cap.get(cv2.CAP_PROP_FPS)
    if fps_video <= 0:
        fps_video = 25.0

    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if largura <= 0 or altura <= 0:
        cap.release()
        raise RuntimeError("Nao foi possivel obter as dimensoes do video.")

    writer = None
    frames_processados = 0
    ids_vistos = set()
    ultimo_frame_id = {}
    frames_por_id = Counter()
    classes_por_id = {}
    intervalos_ausencia = []
    ids_duplicados_por_frame = 0

    inicio = time.perf_counter()

    print("Iniciando rastreamento...")

    try:
        while True:
            sucesso, frame = cap.read()

            if not sucesso:
                break

            frames_processados += 1
            resultado = tracker.track(frame)

            boxes = resultado.boxes
            ids_ativos = []
            classes_ativas = []

            if boxes is not None and boxes.id is not None:
                ids_ativos = boxes.id.int().cpu().tolist()
                classes_ativas = boxes.cls.int().cpu().tolist()

            # Verifica se um mesmo ID aparece mais de uma vez
            # no mesmo frame.
            if len(ids_ativos) != len(set(ids_ativos)):
                ids_duplicados_por_frame += 1

            for track_id, classe_id in zip(ids_ativos, classes_ativas):
                ids_vistos.add(track_id)
                frames_por_id[track_id] += 1

                nome_classe = CLASSES_VEICULOS.get(
                    classe_id, f"classe_{classe_id}"
                )
                classes_por_id.setdefault(track_id, Counter())
                classes_por_id[track_id][nome_classe] += 1

                if track_id in ultimo_frame_id:
                    intervalo = (
                        frames_processados - ultimo_frame_id[track_id]
                    )

                    if intervalo > 1:
                        intervalos_ausencia.append({
                            "id": track_id,
                            "ultimo_frame": ultimo_frame_id[track_id],
                            "frame_retorno": frames_processados,
                            "frames_ausente": intervalo - 1,
                        })

                ultimo_frame_id[track_id] = frames_processados

            # O resultado.plot() desenha caixas e IDs do rastreador.
            frame_saida = resultado.plot()

            # Desenha as trajetorias dos IDs ativos.
            for track_id in set(ids_ativos):
                pontos = tracker.get_trajectory(track_id)

                if len(pontos) >= 2:
                    for i in range(1, len(pontos)):
                        cv2.line(
                            frame_saida,
                            pontos[i - 1],
                            pontos[i],
                            (255, 0, 0),
                            2,
                        )

                estado = tracker.get_vehicle_state(track_id)
                pontos = tracker.get_trajectory(track_id)

                if pontos:
                    x, y = pontos[-1]
                    cv2.putText(
                        frame_saida,
                        estado,
                        (x, max(20, y - 25)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )

            if writer is None:
                codec = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter(
                    str(video_saida),
                    codec,
                    fps_video,
                    (largura, altura),
                )

                if not writer.isOpened():
                    raise RuntimeError(
                        f"Nao foi possivel criar o video: {video_saida}"
                    )

            writer.write(frame_saida)

            if exibir:
                cv2.imshow("RoadVision - Teste de Tracking", frame_saida)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("Processamento interrompido pelo usuario.")
                    break

    finally:
        cap.release()

        if writer is not None:
            writer.release()

        cv2.destroyAllWindows()

    tempo_total = time.perf_counter() - inicio

    # O ID pode reaparecer apos uma ausencia. Isso e um
    # indicio para revisao, nao uma confirmacao de oclusao.
    relatorio = {
        "video_entrada": str(video_path),
        "modelo": str(model_path),
        "video_processado": str(video_saida) if writer is not None else None,
        "frames_processados": frames_processados,
        "fps_original": round(fps_video, 2),
        "resolucao": f"{largura}x{altura}",
        "tempo_processamento_segundos": round(tempo_total, 2),
        "fps_processamento": round(
            frames_processados / tempo_total, 2
        ) if tempo_total > 0 else 0,
        "total_ids_distintos": len(ids_vistos),
        "frames_com_ids_duplicados": ids_duplicados_por_frame,
        "ids": [
            {
                "id": track_id,
                "frames_detectado": frames_por_id[track_id],
                "classe_mais_frequente": (
                    classes_por_id[track_id].most_common(1)[0][0]
                ),
                "frames_por_classe": dict(classes_por_id[track_id]),
            }
            for track_id in sorted(ids_vistos)
        ],
        "ausencias_temporarias": intervalos_ausencia,
        "observacao": (
            "Ausencias e IDs duplicados sao indicadores para revisao. "
            "A consistencia real dos IDs precisa ser verificada "
            "visualmente no video processado."
        ),
    }

    with relatorio_saida.open("w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)

    print("\n===== RESULTADO DO TESTE =====")
    print(f"Frames processados: {frames_processados}")
    print(f"IDs distintos observados: {len(ids_vistos)}")
    print(f"FPS de processamento: {relatorio['fps_processamento']}")
    print(f"Ausencias temporarias registradas: {len(intervalos_ausencia)}")
    print(f"Frames com IDs duplicados: {ids_duplicados_por_frame}")
    print(f"Video processado: {video_saida if writer is not None else 'Nao gerado'}")
    print(f"Relatorio: {relatorio_saida}")


def main():
    parser = argparse.ArgumentParser(
        description="Valida o tracking do RoadVision em videos gravados."
    )
    parser.add_argument(
        "--video",
        required=True,
        help="Caminho para um arquivo de video real.",
    )
    parser.add_argument(
        "--model",
        default=str(MODEL_DEFAULT),
        help="Caminho para os pesos YOLO.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DEFAULT),
        help="Diretorio dos videos e relatorios gerados.",
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="Exibe o video durante o processamento; Q interrompe.",
    )

    args = parser.parse_args()

    processar_video(
        args.video,
        args.model,
        args.output_dir,
        args.display,
    )


if __name__ == "__main__":
    main()
