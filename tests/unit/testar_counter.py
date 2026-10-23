
import pytest

from roadvision.counter import VehicleCounter
from roadvision.detection.contagem_linha_virtual import (
    SENTIDO_1,
    SENTIDO_2,
)


def test_contar_veiculo_apenas_uma_vez():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(1, SENTIDO_1) is True
    assert contador.registrar_cruzamento(1, SENTIDO_1) is False
    assert contador.total_contado() == 1


def test_contar_veiculos_diferentes():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(1, SENTIDO_1) is True
    assert contador.registrar_cruzamento(2, SENTIDO_2) is True
    assert contador.total_contado() == 2


def test_contagem_separada_por_sentido():
    contador = VehicleCounter()

    contador.registrar_cruzamento(1, SENTIDO_1)
    contador.registrar_cruzamento(2, SENTIDO_1)
    contador.registrar_cruzamento(3, SENTIDO_2)

    assert contador.total_por_sentido(SENTIDO_1) == 2
    assert contador.total_por_sentido(SENTIDO_2) == 1


def test_resumo_por_sentido():
    contador = VehicleCounter()

    contador.registrar_cruzamento(1, SENTIDO_1)
    contador.registrar_cruzamento(2, SENTIDO_2)

    assert contador.resumo_por_sentido() == {
        SENTIDO_1: 1,
        SENTIDO_2: 1,
    }


def test_nao_contar_id_nulo():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(None, SENTIDO_1) is False
    assert contador.total_contado() == 0


def test_rejeitar_sentido_invalido():
    contador = VehicleCounter()

    with pytest.raises(ValueError):
        contador.registrar_cruzamento(1, "ida")


def test_nao_contar_sem_sentido_ou_tipo():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(1) is False
    assert contador.total_contado() == 0


def test_contagem_por_tipo_e_sentido():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(
        1, SENTIDO_1, "carro"
    ) is True

    assert contador.total_por_sentido(SENTIDO_1) == 1
    assert contador.total_por_tipo("carro") == 1
