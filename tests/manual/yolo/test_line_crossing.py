import sys
from pathlib import Path

# Caminho da pasta principal do RoadVision
RAIZ_PROJETO = Path(__file__).resolve().parents[3]

# Adiciona a raiz ao caminho de busca do Python
sys.path.insert(0, str(RAIZ_PROJETO))

print("Raiz encontrada:", RAIZ_PROJETO)
print("Pasta src existe:", (RAIZ_PROJETO / "src").is_dir())
print(
    "Arquivo counter.py existe:",
    (RAIZ_PROJETO / "src" / "detection" / "counter.py").is_file()
)

from src.detection.counter import VirtualLineCounter


def test_cruzamento_sentido_positivo():
    contador = VirtualLineCounter((0, 100), (200, 100))

    # Veículo começa acima da linha
    assert contador.atualizar(1, (50, 80)) is None

    # Veículo atravessa a linha
    resultado = contador.atualizar(1, (50, 120))

    assert resultado == "sentido_positivo"


def test_cruzamento_sentido_negativo():
    contador = VirtualLineCounter((0, 100), (200, 100))

    # Veículo começa abaixo da linha
    contador.atualizar(2, (50, 120))

    # Veículo atravessa na direção contrária
    resultado = contador.atualizar(2, (50, 80))

    assert resultado == "sentido_negativo"


def test_nao_conta_o_mesmo_veiculo_duas_vezes():
    contador = VirtualLineCounter((0, 100), (200, 100))

    contador.atualizar(3, (50, 80))

    primeira_contagem = contador.atualizar(3, (50, 120))
    segunda_contagem = contador.atualizar(3, (50, 140))

    assert primeira_contagem is not None
    assert segunda_contagem is None


def test_veiculos_com_ids_diferentes():
    contador = VirtualLineCounter((0, 100), (200, 100))

    contador.atualizar(10, (50, 80))
    contador.atualizar(20, (80, 80))

    resultado_1 = contador.atualizar(10, (50, 120))
    resultado_2 = contador.atualizar(20, (80, 120))

    assert resultado_1 is not None
    assert resultado_2 is not None


def test_linha_diagonal():
    contador = VirtualLineCounter((0, 0), (100, 100))

    contador.atualizar(4, (20, 10))

    resultado = contador.atualizar(4, (10, 20))

    assert resultado is not None
