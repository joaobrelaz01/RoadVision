
from roadvision.database.supabase_client import supabase


CAMPOS_CONTAGEM = (
    "carros",
    "motos",
    "onibus",
    "caminhoes",
)


def validar_contagem(dados: dict) -> list[str]:
    """Retorna os problemas encontrados em uma contagem."""

    erros = []

    campos_obrigatorios = (
        "camera_id",
        "data_hora",
        *CAMPOS_CONTAGEM,
    )

    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            erros.append(f"Campo obrigatório ausente: {campo}")

    for campo in CAMPOS_CONTAGEM:
        valor = dados.get(campo)

        if valor is None:
            continue

        if isinstance(valor, bool) or not isinstance(valor, int):
            erros.append(f"{campo} deve ser um número inteiro")
        elif valor < 0:
            erros.append(f"{campo} não pode ser negativo")

    return erros


def validar_camera(camera_id: str) -> bool:
    """Verifica se a câmera existe no banco."""

    resposta = (
        supabase.table("cameras")
        .select("id")
        .eq("id", camera_id)
        .limit(1)
        .execute()
    )

    return bool(resposta.data)


def verificar_duplicidades() -> list[dict]:
    """Consulta possíveis duplicidades por câmera e horário."""

    resposta = (
        supabase.table("contagens_minuto")
        .select("camera_id,data_hora")
        .execute()
    )

    registros = set()
    duplicidades = []

    for registro in resposta.data:
        chave = (registro["camera_id"], registro["data_hora"])

        if chave in registros:
            duplicidades.append(registro)
        else:
            registros.add(chave)

    return duplicidades
