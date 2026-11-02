from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.models import StatisticsResponse
from backend.app.services.data_service import get_statistics_data

router = APIRouter(prefix="/api/estatisticas", tags=["Estatísticas"])

@router.get("", response_model=StatisticsResponse)
def obter_estatisticas(
    de: Optional[str] = Query(default=None, description="Data início YYYY-MM-DD"),
    ate: Optional[str] = Query(default=None, description="Data fim YYYY-MM-DD"),
    camera_id: Optional[str] = Query(default=None, description="ID ou número da câmera"),
    rodovia: Optional[str] = Query(default=None, description="Nome da rodovia")
):
    """
    Retorna estatísticas REAIS consultadas no banco Supabase filtradas pelo período e câmera.
    Não retorna nenhum valor fictício se não houver dados.
    """
    return get_statistics_data(de=de, ate=ate, camera_id=camera_id, rodovia=rodovia)
