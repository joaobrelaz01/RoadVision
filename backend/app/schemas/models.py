"""
Modelos Pydantic para validação e serialização da API RoadVision.
Utiliza dados estritamente reais consultados do Supabase e do sistema.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class CameraBase(BaseModel):
    id: str
    camera_der_id: Optional[int] = None
    nome: str
    rodovia: str = "SP-055"
    km: str
    municipio: Optional[str] = None
    stream_url: Optional[str] = None
    status: str = "Sem conexão"
    ativa: bool = True
    cadastrada_no_banco: bool = False
    ultima_atualizacao: Optional[str] = "—"

class ContagemMinutoItem(BaseModel):
    id: Optional[int] = None
    camera_id: str
    data_hora: str
    carros: int = 0
    motos: int = 0
    onibus: int = 0
    caminhoes: int = 0
    total: Optional[int] = 0

class ContagemSentidoItem(BaseModel):
    id: Optional[int] = None
    camera_id: str
    data_hora: str
    sentido: str  # "Maranduba" ou "Ubatuba"
    carros: int = 0
    motos: int = 0
    onibus: int = 0
    caminhoes: int = 0
    total: Optional[int] = 0

class DashboardMetrics(BaseModel):
    total_veiculos: int
    cameras_online: int
    cameras_offline: int
    total_cameras: int
    km_monitorados: int
    rodovias_ativas: int
    carros: int
    motos: int
    onibus: int
    caminhoes: int
    is_demo: bool = False

class HourlyFlowItem(BaseModel):
    hora: str
    carros: int
    motos: int
    onibus: int
    caminhoes: int
    total: int

class CategoryShare(BaseModel):
    name: str
    value: int
    color: str

class DashboardResponse(BaseModel):
    metrics: DashboardMetrics
    categories: List[CategoryShare]
    hourly_flow: List[HourlyFlowItem]

class HighwaySummary(BaseModel):
    nome: str
    trecho: str
    km_total: int
    cameras_count: int
    municipios_count: int
    status: str
    detalhes_municipios: List[Dict[str, Any]]

class CameraComparisonItem(BaseModel):
    camera_id: str
    nome_curto: str
    carros: int
    motos: int
    onibus: int
    caminhoes: int
    total: int

class StatisticsResponse(BaseModel):
    categories: List[CategoryShare]
    camera_comparison: List[CameraComparisonItem]
    time_series: List[Dict[str, Any]]
    total_periodo: int

class SystemStatusResponse(BaseModel):
    supabase_connected: bool
    api_status: str
    yolo_processing_status: str
    oracle_cloud_status: str
    active_cameras_limit: int = 2
    active_cameras_count: int
    version: str = "1.0.0"
    last_ping: str
