from playwright.async_api import async_playwright

URL = "http://200.144.30.103:8084/"


async def testar_elementos():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(URL, wait_until="domcontentloaded")

        # Campo de busca das câmeras
        campo_busca = page.locator("#camera-search-input")

        # Itens da lista de câmeras
        cameras = page.locator(".camera-item")

        # Player de vídeo
        video = page.locator("#video-player")

        print("Campo de busca encontrado:", await campo_busca.count())
        print("Itens de câmera encontrados:", await cameras.count())
        print("Player de vídeo encontrado:", await video.count())

        await browser.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(testar_elementos())