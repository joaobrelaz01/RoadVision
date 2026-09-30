from playwright.sync_api import sync_playwright, TimeoutError

class CameraSelector:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
        self.stream_url = None # Variável para guardar o link do vídeo interceptado

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        
        # 🕵️ Manda o Playwright interceptar e "ouvir" todo o tráfego de rede da página
        self.page.on("request", self.intercept_network)
        print("Navegador iniciado.")

    def intercept_network(self, request):
        """Captura qualquer requisição do navegador buscando o stream HLS (.m3u8)"""
        if ".m3u8" in request.url:
            self.stream_url = request.url

    def access_der_portal(self, url: str):
        print(f"Acessando o portal: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle') 

    def search_and_select_camera(self, camera_name: str) -> bool:
        self.stream_url = None # Reseta a URL antiga antes de uma nova busca
        print(f"Buscando pela câmera: {camera_name}...")
        try:
            search_input = self.page.locator('input[type="text"]')
            search_input.wait_for(state='visible', timeout=5000)
            search_input.fill(camera_name)
            search_input.press("Enter")
            
            resultado = self.page.locator(f'text={camera_name}').first
            resultado.wait_for(state='visible', timeout=5000) 
            
            print("Câmera encontrada! Clicando...")
            resultado.click()
            
            # Aguarda 3 segundos para dar tempo do player iniciar o vídeo 
            # e a nossa função intercept_network "pescar" a URL
            self.page.wait_for_timeout(3000) 
            
            return True
            
        except TimeoutError:
            print(f"⚠️ Câmera '{camera_name}' não encontrada ou fora do ar.")
            return False
        except Exception as e:
            print(f"⚠️ Erro inesperado ao buscar câmera: {e}")
            return False

    def get_video_stream_url(self) -> str:
        """Retorna a URL pura que foi interceptada na rede."""
        if self.stream_url:
            print(f"🔗 Stream HLS capturado: {self.stream_url}")
            return self.stream_url
            
        print("Nenhum link de stream (.m3u8) foi interceptado na rede.")
        return None

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("Navegador encerrado.")

if __name__ == "__main__":
    URL_DER = "http://200.144.30.103:8084/"
    CAMERAS_TESTE = ["MARANDUBA", "CAMERA_FANTASMA_999"]
    
    selector = CameraSelector(headless=False) 
    
    try:
        selector.start()
        
        for nome_camera in CAMERAS_TESTE:
            selector.access_der_portal(URL_DER)
            sucesso = selector.search_and_select_camera(nome_camera)
            
            if sucesso:
                url_stream = selector.get_video_stream_url()
            
            print("-" * 40)
            
    finally:
        selector.close()