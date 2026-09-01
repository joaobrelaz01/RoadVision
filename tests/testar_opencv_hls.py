import cv2
import time


BASE_URL = "http://200.144.30.103:8084"

CAMERAS = [
    (36, "KM 055+000", "MARANDUBA"),
    (5, "KM 073+000", "MARANDUBA"),
    (38, "KM 083+500", "MARANDUBA"),
    (37, "KM 092+500", "CARAGUATATUBA"),
    (8, "KM 110+000", "SÃO SEBASTIÃO"),
    (9, "KM 110+000", "MASSAGUAÇU"),
    (10, "KM 136+000", "CARAGUATATUBA"),
    (11, "KM 168+000", "BERTIOGA"),
    (12, "KM 193+000", "SÃO SEBASTIÃO"),
    (13, "KM 211+000", "SÃO SEBASTIÃO"),
    (14, "KM 211+000", "BERTIOGA"),
]


def testar_camera(camera_id, km, sentido):

    stream_url = (
        f"{BASE_URL}/hls/cam_{camera_id}/stream.m3u8"
    )

    print("\n" + "=" * 70)
    print(f"📹 CÂMERA ID: {camera_id}")
    print(f"📍 {km}")
    print(f"↔️ Sentido: {sentido}")
    print(f"🔗 {stream_url}")

    captura = cv2.VideoCapture(stream_url)

    if not captura.isOpened():

        print("❌ OpenCV não conseguiu abrir o stream.")

        captura.release()

        return False

    print("✅ OpenCV abriu o stream!")

    # Damos alguns segundos para o HLS começar a entregar frames
    inicio = time.time()
    frame = None

    while time.time() - inicio < 10:

        sucesso, frame = captura.read()

        if sucesso and frame is not None:

            altura, largura = frame.shape[:2]

            print("🎥 FRAME CAPTURADO!")
            print(f"📐 Resolução: {largura} x {altura}")

            captura.release()

            return True

    print("❌ OpenCV abriu o stream, mas não conseguiu capturar frame.")

    captura.release()

    return False


def main():

    print("=" * 70)
    print("🎥 TESTE OPEN CV + HLS - ROADVISION")
    print("=" * 70)

    resultados = []

    for camera_id, km, sentido in CAMERAS:

        sucesso = testar_camera(
            camera_id,
            km,
            sentido
        )

        resultados.append(
            (camera_id, km, sentido, sucesso)
        )

    print("\n")
    print("=" * 70)
    print("📊 RESULTADO FINAL")
    print("=" * 70)

    funcionando = sum(
        1
        for _, _, _, sucesso in resultados
        if sucesso
    )

    print(
        f"\n🎥 Câmeras testadas: {len(resultados)}"
    )

    print(
        f"✅ OpenCV capturou frame: {funcionando}"
    )

    print(
        f"❌ OpenCV não capturou: "
        f"{len(resultados) - funcionando}"
    )

    print("\nDETALHAMENTO:")
    print("-" * 70)

    for camera_id, km, sentido, sucesso in resultados:

        status = (
            "✅ FRAME OK"
            if sucesso
            else "❌ FALHOU"
        )

        print(
            f"ID {camera_id:02d} | "
            f"{km} | "
            f"{sentido:<15} | "
            f"{status}"
        )


if __name__ == "__main__":
    main()