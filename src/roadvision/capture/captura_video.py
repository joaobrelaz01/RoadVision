# Bibliotecas para leitura de configuração e captura de vídeo.
import json
import cv2
from pathlib import Path

from roadvision.detection.detector_yolo import YOLODetector
from roadvision.tracking import VehicleTracker
from roadvision.capture.tratamento_falha_camera import executar_reconexao
from roadvision.detection.contagem_linha_virtual import LinhaVirtualContagem
from roadvision.counter import VehicleCounter


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
        cameras = carregar_cameras()

        camera_id = 36
        camera = buscar_cameras(cameras, camera_id)

        if camera is None:
            print(f"Câmera com o ID {camera_id} não foi encontrada.")
            return

        print(f"Câmera selecionada: {camera['nome']}")
        print(f"KM: {camera['km']}")
        print(f"Stream: {camera['stream_url']}")

        print("Carregando detector YOLO...")
        detector = YOLODetector()
        tracker = VehicleTracker(detector.model)
        contador = VehicleCounter()
        print("Rastreador de veículos inicializado.")
        print("Contador de veículos inicializado.")

        # Coordenadas provisórias para a câmera 36; ajustar visualmente.
        linha_contagem = LinhaVirtualContagem(
            ponto_inicial=(120, 350),
            ponto_final=(430, 125),
        )
        print("Contagem por linha virtual inicializada.")

        captura = cv2.VideoCapture(camera["stream_url"], cv2.CAP_FFMPEG)

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

                # Reinicia o estado interno do ByteTrack após reconexão.
                detector.model.predictor = None
                print("Captura restaurada. Rastreamento reiniciado.")
                continue

            resultado = tracker.track(frame)
            frames_processados += 1

            # Verifica se cada veículo ativo cruzou a linha virtual.
            for track_id in tracker.get_active_ids():
                trajetoria = tracker.get_trajectory(track_id)

                if len(trajetoria) < 2:
                    continue

                sentido = linha_contagem.verificar_cruzamento(
                    track_id,
                    trajetoria[-2],
                    trajetoria[-1],
                )

                if sentido is not None:
                    registrado = contador.registrar_cruzamento(
                        track_id,
                        sentido,
                    )

                if registrado:
                    print(
                        f"Veículo ID {track_id} contado. "
                        f"Sentido geométrico: {sentido}. "
                        f"Total contado: {contador.total_contado()} | "
                        f"Sentido {sentido}: "
                        f"{contador.total_por_sentido(sentido)}"
                    )

            ids_ativos = tracker.get_active_ids()
            estados = tracker.get_active_states()

            print(
                "Estados dos veículos: "
                + ", ".join(
                    f"ID {track_id}: {estado}"
                    for track_id, estado in estados.items()
                )
            )

            if frames_processados - ultimo_log >= 30:
                print(
                    f"Frames: {frames_processados} | "
                    f"IDs ativos: {ids_ativos} | "
                    f"Total de IDs distintos: {tracker.get_unique_count()} | "
                    f"Veículos contados: {contador.total_contado()}"
                )
                ultimo_log = frames_processados

            frame_analisado = resultado.plot()

            cv2.line(
                frame_analisado,
                linha_contagem.ponto_inicial,
                linha_contagem.ponto_final,
                (0, 255, 255),
                2,
            )
            cv2.putText(
                frame_analisado,
                f"Veiculos contados: {linha_contagem.total_contado()}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            cv2.imshow("RoadVision - Contagem de Veiculos", frame_analisado)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        if captura is not None:
            captura.release()

        cv2.destroyAllWindows()
        print("Recursos da captura liberados.")


if __name__ == "__main__":
    main()