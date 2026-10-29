
from unittest.mock import MagicMock, patch

from roadvision.database import contagens_repository


def test_registrar_contagem():
    dados_esperados = [{
        "id": 10,
        "camera_id": "camera-teste",
        "carros": 3,
        "motos": 1,
        "onibus": 0,
        "caminhoes": 1,
    }]

    with patch.object(
        contagens_repository.supabase,
        "table"
    ) as tabela_mock:
        tabela_mock.return_value.insert.return_value.execute.return_value.data = (
            dados_esperados
        )

        resultado = contagens_repository.registrar_contagem(
            "camera-teste", 3, 1, 0, 1
        )

        assert resultado == dados_esperados
        tabela_mock.assert_called_once_with("contagens_minuto")


def test_listar_contagens():
    dados_esperados = [{
        "id": 10,
        "camera_id": "camera-teste",
        "carros": 3,
        "motos": 1,
        "onibus": 0,
        "caminhoes": 1,
    }]

    with patch.object(
        contagens_repository.supabase,
        "table"
    ) as tabela_mock:
        consulta = tabela_mock.return_value.select.return_value
        consulta.eq.return_value.order.return_value.limit.return_value.execute.return_value.data = (
            dados_esperados
        )

        resultado = contagens_repository.listar_contagens(
            "camera-teste", 5
        )

        assert resultado == dados_esperados
        tabela_mock.assert_called_once_with("contagens_minuto")
