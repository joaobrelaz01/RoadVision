
from roadvision.detection.contagem_linha_virtual import LinhaVirtualContagem


def processar_trajetoria(contador, track_id, pontos):
    """Simula as posições de um veículo ao longo dos frames."""
    for anterior, atual in zip(pontos, pontos[1:]):
        contador.verificar_cruzamento(track_id, anterior, atual)


def test_conta_veiculo_que_cruza_a_linha():
    contador = LinhaVirtualContagem((0, 5), (10, 5))

    processar_trajetoria(contador, 1, [(5, 2), (5, 8)])

    assert contador.total_contado() == 1


def test_nao_conta_veiculo_que_nao_cruza_a_linha():
    contador = LinhaVirtualContagem((0, 5), (10, 5))

    processar_trajetoria(contador, 1, [(1, 1), (3, 2), (5, 3)])

    assert contador.total_contado() == 0


def test_nao_conta_duas_vezes_o_mesmo_id():
    contador = LinhaVirtualContagem((0, 5), (10, 5))

    processar_trajetoria(contador, 1, [(5, 2), (5, 8)])
    processar_trajetoria(contador, 1, [(5, 8), (5, 2)])

    assert contador.total_contado() == 1


def test_conta_dois_ids_diferentes():
    contador = LinhaVirtualContagem((0, 5), (10, 5))

    processar_trajetoria(contador, 1, [(2, 2), (2, 8)])
    processar_trajetoria(contador, 2, [(8, 8), (8, 2)])

    assert contador.total_contado() == 2
