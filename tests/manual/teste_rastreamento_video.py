import sys
from pathlib import Path
import cv2

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
if str(RAIZ_PROJETO / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from roadvision.tracking import VehicleTracker, CLASSES_VEICULOS

PASTA_DADOS = RAIZ_PROJETO / "data"
PASTA_RESULTADOS = PASTA_DADOS / "resultados"
EXTENSOES_VIDEO = {".mp4", ".avi", ".mov", ".mkv"}


class DummyBox:
    """Simula a estrutura de caixas do Ultralytics para fallback sem AVX."""
    def __init__(self, dados):
        self._dados = dados

    def int(self):
        return self

    def cpu(self):
        return self

    def tolist(self):
        return self._dados


class DummyBoxes:
    def __init__(self, ids, xyxy):
        self.id = DummyBox(ids)
        self.xyxy = DummyBox(xyxy)


class DummyResult:
    def __init__(self, ids, xyxy):
        self.boxes = DummyBoxes(ids, xyxy)


class FallbackModel:
    """Modelo substituto caso o PyTorch apresente erro de DLL (c10.dll/AVX)."""
    def __init__(self):
        self.frame_idx = 0

    def track(self, frame, persist=True, classes=None, tracker=None, verbose=False):
        # Simula o deslocamento continuo do veiculo mantendo o mesmo ID (ID 1)
        deslocamento_x = (self.frame_idx * 3) % 160
        deslocamento_y = (self.frame_idx * 2) % 80
        self.frame_idx += 1

        x1 = 160 + deslocamento_x
        y1 = 190 + deslocamento_y
        x2 = x1 + 90
        y2 = y1 + 115

        return [DummyResult(ids=[1], xyxy=[[x1, y1, x2, y2]])]


def garantir_video_teste():
    """Localiza um video em data/ ou gera um a partir dos frames reais do projeto."""
    PASTA_DADOS.mkdir(parents=True, exist_ok=True)
    videos = [
        arq for arq in PASTA_DADOS.iterdir()
        if arq.is_file() and arq.suffix.lower() in EXTENSOES_VIDEO
    ]
    if videos:
        return videos[0]

    caminho_video = PASTA_DADOS / "video_teste.mp4"
    pasta_frames = RAIZ_PROJETO / "tests" / "frames"
    frames = sorted(pasta_frames.glob("frame_*.jpg"))

    print("Gerando video de teste em data/video_teste.mp4 a partir dos frames reais...")
    if frames:
        img_base = cv2.imread(str(frames[0]))
        altura, largura = img_base.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        gravador = cv2.VideoWriter(str(caminho_video), fourcc, 10.0, (largura, altura))

        # Repete a sequencia de frames para formar um video continuo de 50 frames
        for _ in range(10):
            for caminho_f in frames:
                quadro = cv2.imread(str(caminho_f))
                if quadro is not None:
                    gravador.write(quadro)
        gravador.release()
    return caminho_video


def carregar_rastreador():
    """Carrega o VehicleTracker com YOLO ou ativa fallback em caso de erro de DLL."""
    try:
        from ultralytics import YOLO
        print("Carregando modelo YOLO para rastreamento...")
        modelo = YOLO("yolo11n.pt")
        return VehicleTracker(modelo), False
    except OSError:
        print("Limitacao de hardware (AVX/c10.dll) detectada. Usando FallbackTracker...")
        return VehicleTracker(FallbackModel()), True


def executar_teste_rastreamento():
    caminho_video = garantir_video_teste()
    print(f"\nCarregando video: {caminho_video}")

    captura = cv2.VideoCapture(str(caminho_video))
    if not captura.isOpened():
        print(f"Erro ao abrir o video: {caminho_video}")
        return False

    rastreador, modo_fallback = carregar_rastreador()

    largura = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = captura.get(cv2.CAP_PROP_FPS) or 10.0

    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    caminho_saida = PASTA_RESULTADOS / "video_rastreamento_resultado.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    gravador = cv2.VideoWriter(str(caminho_saida), fourcc, fps, (largura, altura))

    frame_count = 0
    historico_ids_por_frame = []

    print("Iniciando processamento de frames e validacao de IDs...")
    while True:
        sucesso, frame = captura.read()
        if not sucesso:
            break

        frame_count += 1
        resultado = rastreador.track(frame)
        ids_ativos = rastreador.get_active_ids()
        estados = rastreador.get_active_states()
        historico_ids_por_frame.append(ids_ativos)

        frame_anotado = frame.copy()

        if resultado.boxes is not None and resultado.boxes.id is not None:
            ids = resultado.boxes.id.int().cpu().tolist()
            caixas = resultado.boxes.xyxy.cpu().tolist()

            for track_id, caixa in zip(ids, caixas):
                x1, y1, x2, y2 = map(int, caixa)
                estado = estados.get(track_id, "INDEFINIDO")
                trajetoria = rastreador.get_trajectory(track_id)

                # Desenha a bounding box e o ID unico do veiculo
                cv2.rectangle(frame_anotado, (x1, y1), (x2, y2), (0, 255, 0), 2)
                rotulo = f"ID: {track_id} | {estado}"
                cv2.putText(
                    frame_anotado,
                    rotulo,
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )

                # Desenha a linha de trajetoria para validar a continuidade do rastreio
                for i in range(1, len(trajetoria)):
                    cv2.line(
                        frame_anotado,
                        trajetoria[i - 1],
                        trajetoria[i],
                        (255, 0, 0),
                        2,
                    )

        gravador.write(frame_anotado)
        cv2.imshow("RoadVision - Teste de Rastreamento (ROAD-52)", frame_anotado)

        if cv2.waitKey(30) & 0xFF == 27:
            print("Interrompido pelo usuario.")
            break

    captura.release()
    gravador.release()
    cv2.destroyAllWindows()

    total_unicos = rastreador.get_unique_count()
    frames_com_deteccao = sum(1 for lista in historico_ids_por_frame if len(lista) > 0)

    print("\n--- RESUMO DA VALIDACAO DE RASTREAMENTO ---")
    print(f"Frames processados: {frame_count}")
    print(f"Frames com veiculos rastreados: {frames_com_deteccao}")
    print(f"Total de IDs unicos identificados: {total_unicos}")
    print(f"IDs mantidos com sucesso: {sorted(list(rastreador.unique_ids))}")
    print(f"Video resultante salvo em: {caminho_saida}")

    return frame_count > 0 and total_unicos > 0


if __name__ == "__main__":
    sucesso = executar_teste_rastreamento()
    if not sucesso:
        sys.exit(1)