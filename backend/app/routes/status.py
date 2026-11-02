from fastapi import APIRouter
from backend.app.schemas.models import SystemStatusResponse
from backend.app.services.data_service import get_system_status

router = APIRouter(prefix="/api/status", tags=["Status do Sistema"])

@router.get("", response_model=SystemStatusResponse)
def status_sistema():
    """Retorna o status dos componentes: Supabase, API, Oracle VM e limites de câmeras."""
    return get_system_status()
