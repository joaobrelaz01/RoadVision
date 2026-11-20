from fastapi import APIRouter
from backend.app.schemas.models import DashboardResponse, AnaliseInteligente
from backend.app.services.data_service import get_dashboard_data

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
def obter_dashboard():
    """Retorna os dados consolidados das últimas 24h para o Dashboard com análise inteligente."""
    return get_dashboard_data()

@router.get("/analise-inteligente", response_model=AnaliseInteligente)
def obter_analise_inteligente():
    """Retorna exclusivamente o bloco analítico qualitativo e estruturado da rodovia."""
    dash = get_dashboard_data()
    return dash.analise_inteligente

