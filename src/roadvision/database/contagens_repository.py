
from datetime import datetime, timezone

from roadvision.database.supabase_client import supabase


def registrar_contagem(
    camera_id: str,
    carros: int,
    motos: int,
    onibus: int,
    caminhoes: int,
):
    """Registra a contagem de veículos de uma câmera."""

    dados = {
        "camera_id": camera_id,
        "data_hora": datetime.now(timezone.utc).isoformat(),
        "carros": carros,
        "motos": motos,
        "onibus": onibus,
        "caminhoes": caminhoes,
    }

    resposta = (
        supabase.table("contagens_minuto")
        .insert(dados)
        .execute()
    )

    return resposta.data


def listar_contagens(camera_id: str, limite: int = 10):
    """Consulta as contagens mais recentes de uma câmera."""

    resposta = (
        supabase.table("contagens_minuto")
        .select("*")
        .eq("camera_id", camera_id)
        .order("data_hora", desc=True)
        .limit(limite)
        .execute()
    )

    return resposta.data
