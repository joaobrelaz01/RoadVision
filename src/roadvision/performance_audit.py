import time
from pathlib import Path

import cv2
import psutil

from roadvision.detection.detector_yolo import YOLODetector


class PerformanceAudit:
    """Mede o desempenho do processamento de IA do RoadVision."""

    def __init__(self, model_path=None):
        self.detector = YOLODetector(model_path)

    def run(self, video_source, max_frames=300):
        """
        Executa a IA sobre uma fonte de vídeo e coleta métricas.

        Args:
            video_source: caminho do vídeo ou URL da câmera.
            max_frames: quantidade máxima de frames processados.
        """

        cap = cv2.VideoCapture(video_source)

        if not cap.isOpened():
            raise RuntimeError(
                f"Não foi possível abrir a fonte de vídeo: {video_source}"
            )

        process = psutil.Process()

        frames_processados = 0
        tempos_frames = []
        uso_cpu = []
        uso_ram = []

        inicio_total = time.perf_counter()

        # Inicializa a medição de CPU.
        process.cpu_percent(interval=None)

        try:
            while frames_processados < max_frames:

                sucesso, frame = cap.read()

                if not sucesso:
                    break

                inicio_frame = time.perf_counter()

                self.detector.detect(frame)

                fim_frame = time.perf_counter()

                tempo_frame = fim_frame - inicio_frame

                tempos_frames.append(tempo_frame)

                uso_cpu.append(process.cpu_percent(interval=None))
                uso_ram.append(
                    process.memory_info().rss / (1024 * 1024)
                )

                frames_processados += 1

        finally:
            cap.release()

        fim_total = time.perf_counter()

        duracao_total = fim_total - inicio_total

        if not tempos_frames:
            raise RuntimeError(
                "Nenhum frame foi processado durante o teste."
            )

        tempo_medio_frame = sum(tempos_frames) / len(tempos_frames)

        fps_medio = (
            1 / tempo_medio_frame
            if tempo_medio_frame > 0
            else 0
        )

        fps_real = (
            frames_processados / duracao_total
            if duracao_total > 0
            else 0
        )

        resultado = {
            "frames_processados": frames_processados,
            "duracao_segundos": round(duracao_total, 2),
            "tempo_medio_frame_ms": round(
                tempo_medio_frame * 1000, 2
            ),
            "fps_medio_ia": round(fps_medio, 2),
            "fps_real": round(fps_real, 2),
            "cpu_media_percent": round(
                sum(uso_cpu) / len(uso_cpu), 2
            ),
            "cpu_max_percent": round(max(uso_cpu), 2),
            "ram_media_mb": round(
                sum(uso_ram) / len(uso_ram), 2
            ),
            "ram_max_mb": round(max(uso_ram), 2),
        }

        return resultado


def main():
    """Executa uma avaliação de desempenho básica."""

    raiz_projeto = Path(__file__).resolve().parents[2]

    modelo = raiz_projeto / "models" / "yolo11n.pt"

    video = "http://200.144.30.103:8084/hls/cam_14/stream.m3u8"

    auditor = PerformanceAudit(modelo)

    resultado = auditor.run(
        video_source=video,
        max_frames=300,
    )

    print("\n===== AUDITORIA DE PERFORMANCE =====")
    print(f"Frames processados: {resultado['frames_processados']}")
    print(f"Duração: {resultado['duracao_segundos']} s")
    print(
        f"Tempo médio por frame: "
        f"{resultado['tempo_medio_frame_ms']} ms"
    )
    print(f"FPS médio da IA: {resultado['fps_medio_ia']}")
    print(f"FPS real: {resultado['fps_real']}")
    print(f"CPU média: {resultado['cpu_media_percent']}%")
    print(f"CPU máxima: {resultado['cpu_max_percent']}%")
    print(f"RAM média: {resultado['ram_media_mb']} MB")
    print(f"RAM máxima: {resultado['ram_max_mb']} MB")


if __name__ == "__main__":
    main()