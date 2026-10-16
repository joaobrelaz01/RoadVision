
from roadvision.counter import VehicleCounter


def test_contar_veiculo_apenas_uma_vez():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(1, "ida") is True
    assert contador.registrar_cruzamento(1, "ida") is False
    assert contador.total_contado() == 1


def test_contar_veiculos_diferentes():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(1, "ida") is True
    assert contador.registrar_cruzamento(2, "volta") is True
    assert contador.total_contado() == 2


def test_contagem_por_sentido():
    contador = VehicleCounter()

    contador.registrar_cruzamento(1, "ida")
    contador.registrar_cruzamento(2, "ida")
    contador.registrar_cruzamento(3, "volta")

    assert contador.total_por_sentido("ida") == 2
    assert contador.total_por_sentido("volta") == 1


def test_nao_contar_id_nulo():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(None, "ida") is False
    assert contador.total_contado() == 0
