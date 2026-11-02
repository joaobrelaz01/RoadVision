from fastapi import APIRouter, Query
from typing import List, Optional
from backend.app.database.supabase_client import get_supabase
from backend.app.schemas.models import ContagemMinutoItem, ContagemSentidoItem

router = APIRouter(prefix="/api/contagens", tags=["Contagens"])

@router.get("", response_model=List[ContagemMinutoItem])
def listar_contagens(
    camera_id: Optional[str] = None,
    limite: int = Query(default=50, ge=1, le=1000)
):
    """Consulta contagens por minuto registradas pelo YOLO no Supabase."""
    client = get_supabase()
    if not client:
        return []
    
    query = client.table("contagens_minuto").select("*").order("data_hora", desc=True).limit(limite)
    if camera_id:
        query = query.eq("camera_id", camera_id)
    
    res = query.execute()
    itens = []
    for r in (res.data or []):
        tot = (r.get("carros", 0) + r.get("motos", 0) + r.get("onibus", 0) + r.get("caminhoes", 0))
        itens.append(ContagemMinutoItem(**r, total=tot))
    return itens

@router.get("/por-sentido", response_model=List[ContagemSentidoItem])
def listar_contagens_sentido(
    camera_id: Optional[str] = None,
    sentido: Optional[str] = None,
    limite: int = Query(default=50, ge=1, le=1000)
):
    """Consulta contagens separadas por sentido (Maranduba / Ubatuba)."""
    client = get_supabase()
    if not client:
        return []
    
    query = client.table("contagens_por_sentido").select("*").order("data_hora", desc=True).limit(limite)
    if camera_id:
        query = query.eq("camera_id", camera_id)
    if sentido:
        query = query.eq("sentido", sentido)
        
    res = query.execute()
    itens = []
    for r in (res.data or []):
        tot = (r.get("carros", 0) + r.get("motos", 0) + r.get("onibus", 0) + r.get("caminhoes", 0))
        itens.append(ContagemSentidoItem(**r, total=tot))
    return itens
