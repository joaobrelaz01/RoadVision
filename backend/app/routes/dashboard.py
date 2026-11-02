from fastapi import APIRouter
from backend.app.schemas.models import DashboardResponse
from backend.app.services.data_service import get_dashboard_data

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
def obter_dashboard():
    """Retorna os dados consolidados das últimas 24h para o Dashboard."""
    return get_dashboard_data()
