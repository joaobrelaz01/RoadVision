import asyncio
import cv2

from playwright.async_api import async_playwright


URL = "http://200.144.30.103:8084/"

NOME_RODOVIA = "Doutor Manoel Hypollito Rego"

CAMERAS = [
    {"km": "055+000", "sentido": ""},
    {"km": "073+000", "sentido": ""},
    
    {"km": "083+500", "sentido": ""},
    {"km": "092+500", "sentido": ""},
    {"km": "110+000", "sentido": "MASSAGUAÇU"},
    {"km": "110+000", "sentido": "SÃO SEBASTIÃO"},
    {"km": "136+000", "sentido": ""},
    {"km": "168+000", "sentido": ""},
    {"km": "193+000", "sentido": ""},
    {"km": "211+000", "sentido": "SÃO SEBASTIÃO"},
    {"km": "211+000", "sentido": "BERTIOGA"},
]


async def testar_camera(page, camera, numero):

    km = camera["km"]
    sentido = camera["sentido"]

    titulo = f"{NOME_RODOVIA} - KM {km}"

    print("\n" + "=" * 60)
    print(f"📹 CÂMERA {numero}/11")
    print(f"📍 {titulo}")
    if sentido:
        print(f"↔️ Sentido: {sentido}")

    # Campo de pesquisa
    busca = page.locator("#camera-search-input")

    await busca.fill(NOME_RODOVIA)

    await page.wait_for_timeout(1000)

    # Localizar resultados
    cameras = page.locator(".camera-item")
    quantidade = await cameras.count()

    print(f"🔎 Resultados encontrados na pesquisa: {quantidade}")

    camera_encontrada = None

    for i in range(quantidade):

        camera_item = cameras.nth(i)

        try:
            texto = await camera_item.inner_text()
        except Exception:
            continue

        if titulo in texto:

            if sentido:
                if sentido not in texto:
                    continue

            camera_encontrada = camera_item
            break

    # Não encontrou
    if camera_encontrada is None:

        print("❌ Câmera não encontrada")

        return {
            "km": km,
            "sentido": sentido,
            "encontrada": False,
            "player": False,
            "stream": "",
            "opencv": False,
        }

    print("✅ Câmera encontrada")

    # Selecionar câmera
    await camera_encontrada.scroll_into_view_if_needed()
    await camera_encontrada.click()

    print("🖱️ Câmera selecionada")

    # Procurar player
    video = page.locator("#video-player")

    try:

        await video.wait_for(
            state="attached",
            timeout=10000
        )

        print("✅ Player encontrado")

    except Exception:

        print("❌ Player não apareceu")

        return {
            "km": km,
            "sentido": sentido,
            "encontrada": True,
            "player": False,
            "stream": "",
            "opencv": False,
        }

    # Esperar o vídeo carregar
    await page.wait_for_timeout(3000)

    # Informações do player
    try:

        video_info = await video.evaluate(
            """
            (el) => ({
                src: el.src,
                currentSrc: el.currentSrc,
                videoWidth: el.videoWidth,
                videoHeight: el.videoHeight,
                readyState: el.readyState,
                paused: el.paused
            })
            """
        )

        print("\n📺 Informações do player:")
        print(video_info)

    except Exception as erro:

        print("⚠️ Erro ao ler player:")
        print(erro)

        video_info = {}

    # Stream
    stream_url = (
        video_info.get("currentSrc")
        or video_info.get("src")
        or ""
    )

    if stream_url:

        print("\n🔗 Stream encontrado:")
        print(stream_url)

    else:

        print("\n❌ Nenhuma URL de stream encontrada")

    # Testar OpenCV
    opencv_ok = False

    if stream_url:

        print("\n🎥 Testando OpenCV...")

        cap = cv2.VideoCapture(stream_url)

        if cap.isOpened():

            sucesso, frame = cap.read()

            if sucesso and frame is not None:

                print("✅ OpenCV conseguiu capturar um frame")

                altura, largura = frame.shape[:2]

                print(
                    f"📐 Resolução capturada: "
                    f"{largura}x{altura}"
                )

                opencv_ok = True

            else:

                print("❌ OpenCV abriu, mas não conseguiu ler frame")

        else:

            print("❌ OpenCV não conseguiu abrir o stream")

        cap.release()

    return {
        "km": km,
        "sentido": sentido,
        "encontrada": True,
        "player": True,
        "stream": stream_url,
        "opencv": opencv_ok,
    }


async def main():

    resultados = []

    async with async_playwright() as p:

        print("🚀 Abrindo navegador...")

        browser = await p.chromium.launch(
            headless=False
        )

        page = await browser.new_page(
            viewport={
                "width": 1400,
                "height": 900
            }
        )

        print("🌐 Acessando DER...")

        await page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        await page.wait_for_timeout(2000)

        print("✅ Site carregado!")

        # Testar todas as câmeras
        for numero, camera in enumerate(CAMERAS, start=1):

            resultado = await testar_camera(
                page,
                camera,
                numero
            )

            resultados.append(resultado)

            # Pequena pausa antes da próxima
            await page.wait_for_timeout(1500)

        # ======================================================
        # RESULTADO FINAL
        # ======================================================

        print("\n")
        print("=" * 70)
        print("📊 RESULTADO FINAL")
        print("=" * 70)

        total = len(resultados)

        encontradas = sum(
            1 for r in resultados
            if r["encontrada"]
        )

        players = sum(
            1 for r in resultados
            if r["player"]
        )

        streams = sum(
            1 for r in resultados
            if r["stream"]
        )

        opencv = sum(
            1 for r in resultados
            if r["opencv"]
        )

        print(f"\n📹 Total de câmeras testadas: {total}")
        print(f"🔎 Câmeras encontradas: {encontradas}")
        print(f"📺 Players encontrados: {players}")
        print(f"🔗 Streams encontrados: {streams}")
        print(f"🎥 OpenCV conseguiu acessar: {opencv}")

        print("\n")
        print("DETALHAMENTO:")
        print("-" * 70)

        for i, resultado in enumerate(resultados, start=1):

            sentido = resultado["sentido"] or "Não informado"

            print(
                f"{i:02d} | "
                f"KM {resultado['km']} | "
                f"{sentido} | "
                f"Encontrada: "
                f"{'SIM' if resultado['encontrada'] else 'NÃO'} | "
                f"Player: "
                f"{'SIM' if resultado['player'] else 'NÃO'} | "
                f"Stream: "
                f"{'SIM' if resultado['stream'] else 'NÃO'} | "
                f"OpenCV: "
                f"{'SIM' if resultado['opencv'] else 'NÃO'}"
            )

        print("\n")
        input("Pressione ENTER para fechar...")

        await browser.close()


asyncio.run(main())