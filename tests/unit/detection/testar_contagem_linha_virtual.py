import pytest

from roadvision.detection.contagem_linha_virtual import (
    LinhaVirtualContagem,
)


def criar_linha():
    return LinhaVirtualContagem((100, 0), (100, 200))


def test_cruzamento_em_um_sentido():
    linha = criar_linha()

    sentido = linha.verificar_cruzamento(
        1, (80, 100), (120, 100)
    )

    assert sentido == "lado_positivo_para_negativo"
    assert linha.total_contado() == 1


def test_cruzamento_no_sentido_oposto():
    linha = criar_linha()

    sentido = linha.verificar_cruzamento(
        2, (120, 100), (80, 100)
    )

    assert sentido == "lado_negativo_para_positivo"
    assert linha.total_contado() == 1


def test_veiculo_nao_cruza_a_linha():
    linha = criar_linha()

    sentido = linha.verificar_cruzamento(
        3, (20, 50), (80, 50)
    )

    assert sentido is None
    assert linha.total_contado() == 0


def test_mesmo_id_nao_e_contado_duas_vezes():
    linha = criar_linha()

    linha.verificar_cruzamento(4, (80, 100), (120, 100))
    repeticao = linha.verificar_cruzamento(
        4, (120, 100), (80, 100)
    )

    assert repeticao is None
    assert linha.total_contado() == 1


def test_rejeita_linha_com_pontos_iguais():
    with pytest.raises(ValueError):
        LinhaVirtualContagem((100, 100), (100, 100))

def test_nao_conta_quando_trajetoria_termina_na_linha():
    linha = criar_linha()

    sentido = linha.verificar_cruzamento(
        5, (80, 100), (100, 100)
    )

    assert sentido is None
    assert linha.total_contado() == 0


def test_nao_conta_quando_trajetoria_comeca_na_linha():
    linha = criar_linha()

    sentido = linha.verificar_cruzamento(
        6, (100, 100), (120, 100)
    )

    assert sentido is None
    assert linha.total_contado() == 0


def test_cruzamento_fora_das_extremidades_nao_e_contado():
    linha = criar_linha()

    sentido = linha.verificar_cruzamento(
        7, (80, 220), (120, 220)
    )

    assert sentido is None
    assert linha.total_contado() == 0