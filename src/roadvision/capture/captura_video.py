# Bibliotecas para leitura de configuração e captura de vídeo.
import json
import cv2
from pathlib import Path

from roadvision.detection.detector_yolo import YOLODetector
from roadvision.tracking import VehicleTracker
from roadvision.capture.tratamento_falha_camera import executar_reconexao


# Caminho do arquivo JSON com as câmeras.
CAMERAS_PATH = (
    Path(__file__).resolve().parents[3]
    / "configs"
    / "cameras"
    / "cameras.json"
)


def carregar_cameras():
    """Carrega a lista de câmeras configuradas."""
    with open(CAMERAS_PATH, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados["cameras"]


def buscar_cameras(cameras, camera_id):
    """Busca uma câmera pelo seu identificador."""
    for camera in cameras:
        if camera["id"] == camera_id:
            return camera

    return None


def main():
    captura = None

    try:
        # Carrega a configuração das câmeras.
        cameras = carregar_cameras()

        # Seleciona a câmera.
        camera_id = 36
        camera = buscar_cameras(cameras, camera_id)

        if camera is None:
            print(f"Câmera com o ID {camera_id} não foi encontrada.")
            return

        print(f"Câmera selecionada: {camera['nome']}")
        print(f"KM: {camera['km']}")
        print(f"Stream: {camera['stream_url']}")

        # Carrega o modelo YOLO uma única vez.
        print("Carregando detector YOLO...")
        detector = YOLODetector()

        # Reutiliza o modelo do detector para rastrear os veículos.
        tracker = VehicleTracker(detector.model)
        print("Rastreador de veículos inicializado.")

        # Abre o stream da câmera.
        captura = cv2.VideoCapture(
            camera["stream_url"],
            cv2.CAP_FFMPEG,
        )

        if not captura.isOpened():
            print("Erro ao abrir a captura de vídeo.")
            return

        print(f"Backend utilizado: {captura.getBackendName()}")
        print("Captura iniciada com sucesso.")
        print("Pressione ESC para sair.")

        frames_processados = 0
        ultimo_log = 0

        while True:
            sucesso, frame = captura.read()

            if not sucesso:
                print("Falha ao capturar frame. Tentando reconectar...")
                captura.release()

                captura = executar_reconexao(camera)

                if captura is None:
                    print("Não foi possível reconectar. Encerrando.")
                    break

                # O fluxo de vídeo foi reiniciado.
                # Resetamos o estado interno do ByteTrack para evitar
                # misturar o estado anterior com o novo stream.
                detector.model.predictor = None

                print("Captura restaurada. Rastreamento reiniciado.")
                continue

            # O rastreador recebe cada frame capturado.
            resultado = tracker.track(frame)
            frames_processados += 1

            ids_ativos = tracker.get_active_ids()

            estados = tracker.get_active_states()

            print(
                "Estados dos veículos: "
                + ", ".join(
                    f"ID {track_id}: {estado}"
                    for track_id, estado in estados.items()
                )
            )

            # Registra informações no terminal a cada 30 frames.
            if frames_processados - ultimo_log >= 30:
                print(
                    f"Frames: {frames_processados} | "
                    f"IDs ativos: {ids_ativos} | "
                    f"Total de IDs distintos: "
                    f"{tracker.get_unique_count()}"
                )
                ultimo_log = frames_processados

            # Exibe as caixas e os IDs atribuídos pelo rastreador.
            frame_analisado = resultado.plot()
            cv2.imshow("RoadVision - Rastreamento", frame_analisado)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        # Libera os recursos mesmo se ocorrer um erro.
        if captura is not None:
            captura.release()

        cv2.destroyAllWindows()
        print("Recursos da captura liberados.")


if __name__ == "__main__":
    main()