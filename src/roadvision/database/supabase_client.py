
import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

_url = os.getenv("SUPABASE_URL")
_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not _url or not _key:
    raise RuntimeError(
        "SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY "
        "precisam estar configuradas no arquivo .env"
    )

supabase: Client = create_client(_url, _key)


def testar_conexao() -> bool:
    """Verifica a conexão consultando a tabela de câmeras."""
    supabase.table("cameras").select("id").limit(1).execute()
    return True
