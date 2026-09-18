import requests


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


def testar_stream(camera_id, km, sentido):

    url = f"{BASE_URL}/hls/cam_{camera_id}/stream.m3u8"

    print("\n" + "=" * 70)
    print(f"📹 CÂMERA ID: {camera_id}")
    print(f"📍 {km}")
    print(f"↔️ Sentido: {sentido}")
    print(f"🔗 {url}")

    try:

        resposta = requests.get(
            url,
            timeout=10
        )

        print(f"📡 HTTP Status: {resposta.status_code}")
        print(
            f"📦 Content-Type: "
            f"{resposta.headers.get('Content-Type')}"
        )

        if resposta.status_code == 200:

            conteudo = resposta.text

            if "#EXTM3U" in conteudo:

                print("✅ PLAYLIST HLS VÁLIDA!")

                print("\n📋 Conteúdo inicial:")

                print(
                    conteudo[:500]
                )

                return True

            else:

                print(
                    "⚠️ Respondeu 200, "
                    "mas não parece ser uma playlist HLS."
                )

        else:

            print("❌ Stream não respondeu com HTTP 200.")

    except requests.exceptions.RequestException as erro:

        print(f"❌ Erro de conexão: {erro}")

    return False


def main():

    print("=" * 70)
    print("🔎 TESTE DIRETO DOS STREAMS HLS - ROADVISION")
    print("=" * 70)

    resultados = []

    for camera_id, km, sentido in CAMERAS:

        sucesso = testar_stream(
            camera_id,
            km,
            sentido
        )

        resultados.append({
            "id": camera_id,
            "km": km,
            "sentido": sentido,
            "sucesso": sucesso
        })

    # =========================================================
    # RESULTADO FINAL
    # =========================================================

    print("\n")
    print("=" * 70)
    print("📊 RESULTADO FINAL")
    print("=" * 70)

    funcionando = sum(
        1 for resultado in resultados
        if resultado["sucesso"]
    )

    print(
        f"\n🎥 Streams testados: {len(resultados)}"
    )

    print(
        f"✅ Streams funcionando: {funcionando}"
    )

    print(
        f"❌ Streams com problema: "
        f"{len(resultados) - funcionando}"
    )

    print("\nDETALHAMENTO:")
    print("-" * 70)

    for resultado in resultados:

        status = (
            "✅ FUNCIONANDO"
            if resultado["sucesso"]
            else "❌ FALHOU"
        )

        print(
            f"ID {resultado['id']:02d} | "
            f"{resultado['km']} | "
            f"{resultado['sentido']:<15} | "
            f"{status}"
        )


if __name__ == "__main__":
    main()