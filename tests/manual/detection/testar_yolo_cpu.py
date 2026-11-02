
import cv2
import torch

from pathlib import Path
from roadvision.detection.detector_yolo import YOLODetector


def main():
    raiz = Path(__file__).resolve().parents[3]
    imagem_path = raiz / "tests" / "manual" / "cameras" / "frame_camera_36.jpg"

    print("GPU disponível:", torch.cuda.is_available())
    print("Dispositivo configurado: CPU")

    if not imagem_path.exists():
        print(f"Imagem não encontrada: {imagem_path}")
        print("Coloque um frame da câmera 36 nesse caminho.")
        return

    frame = cv2.imread(str(imagem_path))

    if frame is None:
        print("Não foi possível carregar a imagem.")
        return

    detector = YOLODetector()

    resultado, frame_processado, tempo = detector.processar_frame(frame)
    deteccoes = detector.validar_deteccoes(resultado)

    print(f"Tempo de inferência: {tempo:.2f} ms")
    print(f"Total de veículos detectados: {len(deteccoes)}")
    print("Detecções:", deteccoes)

    saida = raiz / "tests" / "manual" / "detection" / "frame_processado.jpg"
    cv2.imwrite(str(saida), frame_processado)

    print(f"Frame processado salvo em: {saida}")


if __name__ == "__main__":
    main()
