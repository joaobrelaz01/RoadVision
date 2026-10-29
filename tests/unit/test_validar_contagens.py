
from unittest.mock import patch

from roadvision.database.validar_contagens import (
    validar_contagem,
    validar_camera,
    verificar_duplicidades,
)


def contagem_valida():
    return {
        "camera_id": "camera-teste",
        "data_hora": "2026-10-29T12:00:00+00:00",
        "carros": 10,
        "motos": 2,
        "onibus": 1,
        "caminhoes": 3,
    }


def test_contagem_valida():
    assert validar_contagem(contagem_valida()) == []


def test_detecta_campo_obrigatorio_ausente():
    dados = contagem_valida()
    del dados["camera_id"]

    erros = validar_contagem(dados)

    assert any("camera_id" in erro for erro in erros)


def test_detecta_quantidade_negativa():
    dados = contagem_valida()
    dados["carros"] = -1

    erros = validar_contagem(dados)

    assert any("negativo" in erro for erro in erros)


def test_detecta_valor_nao_inteiro():
    dados = contagem_valida()
    dados["motos"] = 2.5

    erros = validar_contagem(dados)

    assert any("inteiro" in erro for erro in erros)


def test_validar_camera_existente():
    with patch(
        "roadvision.database.validar_contagens.supabase"
    ) as banco:
        banco.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value.data = [
            {"id": "camera-teste"}
        ]

        assert validar_camera("camera-teste") is True


def test_validar_camera_inexistente():
    with patch(
        "roadvision.database.validar_contagens.supabase"
    ) as banco:
        banco.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value.data = []

        assert validar_camera("camera-inexistente") is False


def test_detectar_duplicidades():
    registro = {
        "camera_id": "camera-teste",
        "data_hora": "2026-10-29T12:00:00+00:00",
    }

    with patch(
        "roadvision.database.validar_contagens.supabase"
    ) as banco:
        banco.table.return_value.select.return_value.execute.return_value.data = [
            registro,
            registro,
        ]

        resultado = verificar_duplicidades()

        assert len(resultado) == 1
