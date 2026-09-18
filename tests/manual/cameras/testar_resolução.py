import cv2


CAMERAS = {
    "KM 055+000": "http://200.144.30.103:8084/hls/cam_36/stream.m3u8",
    "KM 073+000": "http://200.144.30.103:8084/hls/cam_5/stream.m3u8",
    "KM 083+500": "http://200.144.30.103:8084/hls/cam_38/stream.m3u8",
    "KM 092+500": "http://200.144.30.103:8084/hls/cam_37/stream.m3u8",
    "KM 110+000 - 1": "http://200.144.30.103:8084/hls/cam_8/stream.m3u8",
    "KM 110+000 - 2": "http://200.144.30.103:8084/hls/cam_9/stream.m3u8",
    "KM 136+000": "http://200.144.30.103:8084/hls/cam_10/stream.m3u8",
    "KM 168+000": "http://200.144.30.103:8084/hls/cam_11/stream.m3u8",
    "KM 193+000": "http://200.144.30.103:8084/hls/cam_12/stream.m3u8",
    "KM 211+000 - 1": "http://200.144.30.103:8084/hls/cam_13/stream.m3u8",
    "KM 211+000 - 2": "http://200.144.30.103:8084/hls/cam_14/stream.m3u8",
}


def verificar_resolucao(nome, url):
    print(f"\nTestando: {nome}")

    captura = cv2.VideoCapture(url)

    if not captura.isOpened():
        print("❌ Não foi possível conectar.")
        return

    sucesso, frame = captura.read()

    if not sucesso:
        print("❌ Não foi possível obter um frame.")
        captura.release()
        return

    altura, largura = frame.shape[:2]

    print(f"✅ Conectada")
    print(f"   Resolução: {largura} x {altura}")

    captura.release()


def main():
    print("=== RoadVision - Teste de resolução das câmeras ===")

    for nome, url in CAMERAS.items():
        verificar_resolucao(nome, url)

    print("\n=== Teste finalizado ===")


if __name__ == "__main__":
    main()