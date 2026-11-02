from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.app.database.supabase_client import get_supabase
from backend.app.services.data_service import get_todas_cameras

router = APIRouter(prefix="/api/relatorios", tags=["Relatórios"])

@router.get("")
def obter_relatorio(
    de: Optional[str] = Query(default=None, description="Data início YYYY-MM-DD"),
    ate: Optional[str] = Query(default=None, description="Data fim YYYY-MM-DD"),
    camera_id: Optional[str] = Query(default=None, description="ID da câmera"),
    sentido: Optional[str] = Query(default=None, description="Sentido Maranduba ou Ubatuba")
):
    """
    Gera dados históricos REAIS a partir da tabela contagens_por_sentido no Supabase.
    Zero dados fictícios.
    """
    client = get_supabase()
    dados_tabela: List[Dict[str, Any]] = []

    # Sanitização segura dos parâmetros
    de_str = de if isinstance(de, str) and de.strip() else None
    ate_str = ate if isinstance(ate, str) and ate.strip() else None
    cam_str = camera_id if isinstance(camera_id, str) and camera_id.strip() else None
    sentido_str = sentido if isinstance(sentido, str) and sentido.strip() else None

    # Mapeamento amigável das câmeras
    cameras_list = get_todas_cameras()
    mapa_cameras = {}
    for c in cameras_list:
        mapa_cameras[c.id] = f"ID {c.camera_der_id or c.id} — {c.nome} ({c.km})"
        if c.camera_der_id:
            mapa_cameras[str(c.camera_der_id)] = f"ID {c.camera_der_id} — {c.nome} ({c.km})"

    if client:
        try:
            query = client.table("contagens_por_sentido").select("*").order("data_hora", desc=True)
            
            if de_str:
                query = query.gte("data_hora", f"{de_str}T00:00:00")
            if ate_str:
                query = query.lte("data_hora", f"{ate_str}T23:59:59")
            if cam_str and cam_str not in ("Todas", "todas"):
                query = query.eq("camera_id", cam_str)
            if sentido_str and sentido_str not in ("Todos", "todos"):
                query = query.eq("sentido", sentido_str)

            res = query.limit(500).execute()
            if res and res.data:
                for row in res.data:
                    c = row.get("carros", 0) or 0
                    m = row.get("motos", 0) or 0
                    o = row.get("onibus", 0) or 0
                    k = row.get("caminhoes", 0) or 0
                    tot = c + m + o + k
                    cid = str(row.get("camera_id", ""))
                    
                    dt_raw = row.get("data_hora", "")
                    try:
                        dt = datetime.fromisoformat(dt_raw.replace("Z", "+00:00"))
                        dt_formatada = dt.strftime("%d/%m/%Y %H:%M:%S")
                    except Exception:
                        dt_formatada = dt_raw

                    dados_tabela.append({
                        "id": row.get("id"),
                        "data_hora": dt_formatada,
                        "data_hora_raw": dt_raw,
                        "camera_id": cid,
                        "camera": mapa_cameras.get(cid, f"Câmera {cid[:8]}"),
                        "sentido": row.get("sentido", "Não especificado"),
                        "carros": c,
                        "motos": m,
                        "onibus": o,
                        "caminhoes": k,
                        "total": tot
                    })
        except Exception as e:
            print(f"[Relatórios] Erro ao consultar Supabase: {e}")

    return {
        "filtros": {"de": de_str, "ate": ate_str, "camera_id": cam_str, "sentido": sentido_str},
        "total_registros": len(dados_tabela),
        "registros": dados_tabela
    }
