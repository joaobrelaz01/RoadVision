import pytest

from roadvision.counter import VehicleCounter


@pytest.mark.parametrize(
    "tipo",
    ["carro", "moto", "onibus", "caminhao"],
)
def test_contagem_por_tipo(tipo):
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(
        1, vehicle_type=tipo
    ) is True

    assert contador.total_por_tipo(tipo) == 1


def test_nao_contar_id_repetido():
    contador = VehicleCounter()

    assert contador.registrar_cruzamento(
        1, vehicle_type="carro"
    ) is True

    assert contador.registrar_cruzamento(
        1, vehicle_type="carro"
    ) is False

    assert contador.total_contado() == 1
    assert contador.total_por_tipo("carro") == 1
