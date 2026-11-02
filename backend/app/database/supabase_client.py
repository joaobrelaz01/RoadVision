"""
Conexão oficial do Backend FastAPI com o Supabase.
"""
from typing import Optional
from supabase import create_client, Client
from backend.app.config import SUPABASE_URL, SUPABASE_KEY

_supabase_client: Optional[Client] = None

def get_supabase() -> Optional[Client]:
    """Retorna a instância singleton do cliente Supabase."""
    global _supabase_client
    if _supabase_client is None and SUPABASE_URL and SUPABASE_KEY:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"[Supabase] Erro ao conectar: {e}")
            _supabase_client = None
    return _supabase_client

def check_supabase_health() -> bool:
    """Verifica se a conexão com o Supabase está respondendo."""
    client = get_supabase()
    if not client:
        return False
    try:
        res = client.table("cameras").select("id").limit(1).execute()
        return res is not None
    except Exception as e:
        print(f"[Supabase Health] Falha: {e}")
        return False
