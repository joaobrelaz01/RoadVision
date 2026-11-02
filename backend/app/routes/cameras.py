from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.schemas.models import CameraBase, HighwaySummary
from backend.app.services.data_service import get_todas_cameras, get_rodovia_summary

router = APIRouter(prefix="/api", tags=["Câmeras e Rodovias"])

@router.get("/cameras", response_model=List[CameraBase])
def listar_cameras():
    """Lista todas as 11 câmeras cadastradas da SP-055 com seus status e metadados."""
    return get_todas_cameras()

@router.get("/cameras/{camera_id}", response_model=CameraBase)
def obter_camera(camera_id: str):
    """Busca detalhes de uma câmera específica por ID ou ID DER."""
    cameras = get_todas_cameras()
    for c in cameras:
        if c.id == camera_id or str(c.camera_der_id) == camera_id:
            return c
    raise HTTPException(status_code=404, detail="Câmera não encontrada")

@router.get("/rodovias", response_model=List[HighwaySummary])
def listar_rodovias():
    """Retorna os dados consolidados das rodovias monitoradas (SP-055)."""
    return [get_rodovia_summary()]
