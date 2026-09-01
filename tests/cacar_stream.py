import asyncio
from playwright.async_api import async_playwright


URL = "http://200.144.30.103:8084/"

NOME_CAMERA = "Doutor Manoel Hypollito Rego"
KM_CAMERA = "110+000"
SENTIDO_CAMERA = "SÃO SEBASTIÃO"


async def main():

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

        # =====================================================
        # CAÇADOR DE REQUISIÇÕES
        # =====================================================

        def verificar_requisicao(request):

            url = request.url.lower()

            palavras = [
                "stream",
                "video",
                "vide",
                "camera",
                "m3u8",
                "mjpeg",
                "mp4",
                "mpeg",
                "hls",
                ".ts",
                "media",
                "playlist",
                "live",
                "segment",
                "blob"
            ]

            if any(palavra in url for palavra in palavras):

                print("\n🎯 POSSÍVEL REQUISIÇÃO DE VÍDEO")
                print(f"➡️ Método: {request.method}")
                print(f"➡️ URL: {request.url}")

        page.on(
            "request",
            verificar_requisicao
        )

        # =====================================================
        # ACESSAR DER
        # =====================================================

        print("🌐 Acessando DER...")

        await page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        await page.wait_for_timeout(2000)

        print("✅ Site carregado!")

        # =====================================================
        # PESQUISAR CÂMERA
        # =====================================================

        busca = page.locator(
            "#camera-search-input"
        )

        await busca.fill(
            NOME_CAMERA
        )

        await page.wait_for_timeout(1000)

        cameras = page.locator(
            ".camera-item"
        )

        quantidade = await cameras.count()

        print(
            f"🔎 Câmeras encontradas: {quantidade}"
        )

        camera_encontrada = None

        for i in range(quantidade):

            camera = cameras.nth(i)

            try:
                texto = await camera.inner_text()
            except Exception:
                continue

            if (
                f"{NOME_CAMERA} - KM {KM_CAMERA}"
                in texto
                and SENTIDO_CAMERA
                in texto
            ):

                camera_encontrada = camera

                print("\n✅ Câmera encontrada!")
                print(texto)

                break

        if camera_encontrada is None:

            print("❌ Câmera não encontrada")

            await browser.close()

            return

        # =====================================================
        # SELECIONAR CÂMERA
        # =====================================================

        print("\n🖱️ Selecionando câmera...")

        await camera_encontrada.scroll_into_view_if_needed()

        await camera_encontrada.click()

        print(
            "✅ Câmera selecionada!"
        )

        # =====================================================
        # DEIXAR A REDE SER OBSERVADA
        # =====================================================

        print("\n👀 Observando requisições...")
        print(
            "⏳ Aguarde aproximadamente 15 segundos..."
        )

        await page.wait_for_timeout(
            15000
        )

        # =====================================================
        # INSPECIONAR PLAYER
        # =====================================================

        video = page.locator(
            "#video-player"
        )

        try:

            info = await video.evaluate(
                """
                el => ({
                    src: el.src,
                    currentSrc: el.currentSrc,
                    readyState: el.readyState,
                    videoWidth: el.videoWidth,
                    videoHeight: el.videoHeight,
                    paused: el.paused
                })
                """
            )

            print("\n📺 INFORMAÇÕES DO PLAYER")
            print("=" * 60)

            for chave, valor in info.items():

                print(
                    f"{chave}: {valor}"
                )

        except Exception as erro:

            print(
                f"\n Não foi possível ler o player: {erro}"
            )

        print("\n" + "=" * 60)
        print("🏁 FIM DO TESTE")
        print("=" * 60)

        input(
            "\nPressione ENTER para fechar..."
        )

        await browser.close()


asyncio.run(main())