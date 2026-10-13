from ultralytics import YOLO

def carregar_modelo(peso: str = "yolo11n.pt"):
    """
    Carrega o modelo YOLO.
    O download do arquivo .pt é feito automaticamente pela biblioteca se ele não existir localmente.
    """
    print(f"🔄 Carregando modelo YOLO ({peso})...")
    modelo = YOLO(peso)
    print("✅ Modelo carregado com sucesso!")
    return modelo

if __name__ == "__main__":
    # Teste rápido para garantir o carregamento correto ao executar este arquivo diretamente
    carregar_modelo()