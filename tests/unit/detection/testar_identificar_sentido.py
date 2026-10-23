
from roadvision.detection.contagem_linha_virtual import (
    LinhaVirtualContagem,
    SENTIDO_1,
    SENTIDO_2,
)
from roadvision.detection.identificar_sentido import IdentificadorSentido


def criar_identificador():
    linha = LinhaVirtualContagem((100, 0), (100, 200))
    return IdentificadorSentido(linha)


def test_identifica_sentido_1():
    identificador = criar_identificador()

    trajetoria = [(120, 100), (80, 100)]

    assert identificador.identificar(trajetoria) == SENTIDO_1


def test_identifica_sentido_2():
    identificador = criar_identificador()

    trajetoria = [(80, 100), (120, 100)]

    assert identificador.identificar(trajetoria) == SENTIDO_2


def test_trajetoria_insuficiente():
    identificador = criar_identificador()

    assert identificador.identificar([]) is None
    assert identificador.identificar([(80, 100)]) is None


def test_sem_cruzamento():
    identificador = criar_identificador()

    trajetoria = [(50, 50), (60, 60), (70, 70)]

    assert identificador.identificar(trajetoria) is None


def test_cruzamento_em_trajetoria_com_varios_pontos():
    identificador = criar_identificador()

    trajetoria = [(80, 50), (90, 60), (110, 70), (120, 80)]

    assert identificador.identificar(trajetoria) == SENTIDO_2
