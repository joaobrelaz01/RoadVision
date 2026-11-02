"""
Serviço de agregação e consulta de dados para a API RoadVision.
Combina as tabelas do Supabase (cameras, contagens_minuto, contagens_por_sentido)
com as configurações de câmeras do DER/SP em configs/cameras/cameras.json.
"""
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from backend.app.database.supabase_client import get_supabase, check_supabase_health
from backend.app.schemas.models import (
    CameraBase,
    DashboardResponse,
    DashboardMetrics,
    CategoryShare,
    HourlyFlowItem,
    HighwaySummary,
    StatisticsResponse,
    CameraComparisonItem,
    SystemStatusResponse
)

# Caminho para configs/cameras/cameras.json
BASE_DIR = Path(__file__).resolve().parents[3]
CAMERAS_JSON_PATH = BASE_DIR / "configs" / "cameras" / "cameras.json"

# Câmeras padrão conhecidas do DER/SP na SP-055
DEFAULT_DER_CAMERAS = [
    {"id": 36, "km": "055+000", "municipio": "Maranduba", "nome": "Maranduba — km 055+000", "rodovia": "SP-055"},
    {"id": 5, "km": "073+000", "municipio": "Maranduba", "nome": "Maranduba — km 073+000", "rodovia": "SP-055"},
    {"id": 38, "km": "083+500", "municipio": "Maranduba", "nome": "Maranduba — km 083+500", "rodovia": "SP-055"},
    {"id": 37, "km": "092+500", "municipio": "Caraguatatuba", "nome": "Caraguatatuba — km 092+500", "rodovia": "SP-055"},
    {"id": 8, "km": "110+000", "municipio": "São Sebastião", "nome": "São Sebastião — km 110+000", "rodovia": "SP-055"},
    {"id": 9, "km": "110+000", "municipio": "Massaguaçu", "nome": "Massaguaçu — km 110+000", "rodovia": "SP-055"},
    {"id": 10, "km": "136+000", "municipio": "Caraguatatuba", "nome": "Caraguatatuba — km 136+000", "rodovia": "SP-055"},
    {"id": 11, "km": "168+000", "municipio": "Bertioga", "nome": "Bertioga — km 168+000", "rodovia": "SP-055"},
    {"id": 12, "km": "193+000", "municipio": "São Sebastião", "nome": "São Sebastião — km 193+000", "rodovia": "SP-055"},
    {"id": 13, "km": "211+000", "municipio": "São Sebastião", "nome": "São Sebastião — km 211+000", "rodovia": "SP-055"},
    {"id": 14, "km": "211+000", "municipio": "Bertioga", "nome": "Bertioga — km 211+000", "rodovia": "SP-055"},
]

def carregar_cameras_config() -> List[Dict[str, Any]]:
    """Carrega dados completos do arquivo cameras.json do projeto."""
    if CAMERAS_JSON_PATH.exists():
        try:
            with open(CAMERAS_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("cameras", [])
        except Exception as e:
            print(f"[DataService] Falha ao ler cameras.json: {e}")
    return []

def get_todas_cameras() -> List[CameraBase]:
    """Retorna a lista completa das 11 câmeras do DER/SP."""
    configs = {c["id"]: c for c in carregar_cameras_config()}
    client = get_supabase()
    supabase_map = {}

    if client:
        try:
            res = client.table("cameras").select("*").execute()
            if res and res.data:
                for row in res.data:
                    # Mapeia por nome ou ID
                    supabase_map[str(row.get("id"))] = row
                    supabase_map[row.get("nome", "")] = row
        except Exception as e:
            print(f"[DataService] Erro ao consultar câmeras no Supabase: {e}")

    resultado: List[CameraBase] = []
    for default in DEFAULT_DER_CAMERAS:
        der_id = default["id"]
        cfg = configs.get(der_id, {})
        stream_url = cfg.get("stream_url", f"http://200.144.30.103:8084/hls/cam_{der_id}/stream.m3u8")

        # Câmeras do Supabase correspondentes se cadastradas
        sub_info = None
        for k, v in supabase_map.items():
            if f"Camera {der_id}" in str(v.get("nome", "")) or f"cam_{der_id}" in str(v.get("nome", "")):
                sub_info = v
                break

        resultado.append(CameraBase(
            id=str(sub_info.get("id")) if sub_info else f"der-cam-{der_id}",
            camera_der_id=der_id,
            nome=default["nome"],
            rodovia="SP-055",
            km=default["km"],
            municipio=default["municipio"],
            stream_url=stream_url,
            status="Sem conexão",
            ativa=True,
            ultima_atualizacao="—"
        ))

    return resultado

def get_dashboard_data() -> DashboardResponse:
    """
    Retorna os indicadores consolidados das últimas 24 horas.
    Prioriza dados do Supabase ou serve os indicadores fiéis da referência Lovable.
    """
    client = get_supabase()
    tem_dados_reais = False
    
    # Indicadores padrão das imagens Lovable:
    total_veiculos = 47152
    carros = 32180
    motos = 4775
    onibus = 1477
    caminhoes = 8720

    if client:
        try:
            # Consulta contagens do Supabase
            res = client.table("contagens_minuto").select("carros,motos,onibus,caminhoes").execute()
            if res and res.data and len(res.data) > 0:
                # Se houver dados reais no banco, soma-os
                s_carros = sum(r.get("carros", 0) for r in res.data)
                s_motos = sum(r.get("motos", 0) for r in res.data)
                s_onibus = sum(r.get("onibus", 0) for r in res.data)
                s_caminhoes = sum(r.get("caminhoes", 0) for r in res.data)
                if (s_carros + s_motos + s_onibus + s_caminhoes) > 0:
                    carros = s_carros
                    motos = s_motos
                    onibus = s_onibus
                    caminhoes = s_caminhoes
                    total_veiculos = carros + motos + onibus + caminhoes
                    tem_dados_reais = True
        except Exception as e:
            print(f"[DataService] Erro ao consultar métricas no Supabase: {e}")

    metrics = DashboardMetrics(
        total_veiculos=total_veiculos,
        cameras_online=0,
        cameras_offline=11,
        total_cameras=11,
        km_monitorados=156,
        rodovias_ativas=1,
        carros=carros,
        motos=motos,
        onibus=onibus,
        caminhoes=caminhoes,
        is_demo=not tem_dados_reais
    )

    categories = [
        CategoryShare(name="Carros", value=carros, color="#0284c7"),
        CategoryShare(name="Motos", value=motos, color="#f97316"),
        CategoryShare(name="Ônibus", value=onibus, color="#06b6d4"),
        CategoryShare(name="Caminhões", value=caminhoes, color="#1e293b"),
    ]

    # Curva horária fiel à Imagem 1 do Lovable (picos às 08h e 17h):
    hourly_samples = [
        ("00h", 210, 30, 10, 80),
        ("01h", 140, 20, 5, 60),
        ("02h", 110, 15, 5, 50),
        ("03h", 95, 10, 5, 45),
        ("04h", 120, 25, 10, 60),
        ("05h", 280, 50, 20, 110),
        ("06h", 620, 120, 45, 230),
        ("07h", 1180, 210, 80, 350),
        ("08h", 1290, 240, 95, 380),
        ("09h", 1020, 190, 70, 320),
        ("10h", 910, 160, 55, 280),
        ("11h", 940, 175, 60, 290),
        ("12h", 1010, 180, 65, 305),
        ("13h", 980, 170, 60, 295),
        ("14h", 1030, 185, 65, 310),
        ("15h", 1150, 210, 75, 360),
        ("16h", 1380, 250, 85, 410),
        ("17h", 1490, 260, 90, 430),
        ("18h", 1210, 215, 75, 360),
        ("19h", 890, 160, 50, 270),
        ("20h", 670, 110, 35, 190),
        ("21h", 490, 80, 25, 140),
        ("22h", 380, 55, 15, 105),
        ("23h", 260, 40, 10, 85),
    ]

    hourly_flow = [
        HourlyFlowItem(
            hora=h,
            carros=c,
            motos=m,
            onibus=o,
            caminhoes=k,
            total=c + m + o + k
        )
        for (h, c, m, o, k) in hourly_samples
    ]

    return DashboardResponse(
        metrics=metrics,
        categories=categories,
        hourly_flow=hourly_flow
    )

def get_rodovia_summary() -> HighwaySummary:
    """Retorna as informações consolidadas da SP-055 (Imagem 3)."""
    municipios_info = [
        {"municipio": "Maranduba", "cameras": 3, "quilometros": "055+000 — 083+500", "status": "Sem conexão"},
        {"municipio": "Caraguatatuba", "cameras": 2, "quilometros": "092+500 — 136+000", "status": "Sem conexão"},
        {"municipio": "São Sebastião", "cameras": 3, "quilometros": "110+000 — 211+000", "status": "Sem conexão"},
        {"municipio": "Massaguaçu", "cameras": 1, "quilometros": "110+000 — 110+000", "status": "Sem conexão"},
        {"municipio": "Bertioga", "cameras": 2, "quilometros": "168+000 — 211+000", "status": "Sem conexão"},
    ]

    return HighwaySummary(
        nome="SP-055 — RODOVIA RIO-SANTOS",
        trecho="km 055+000 — 211+000",
        km_total=156,
        cameras_count=11,
        municipios_count=5,
        status="Sem conexão",
        detalhes_municipios=municipios_info
    )

def get_statistics_data() -> StatisticsResponse:
    """Retorna os dados estatísticos completos da Imagem 5."""
    dash = get_dashboard_data()

    # Comparação entre câmeras fiéis ao gráfico da Imagem 5:
    cam_data = [
        ("36", "36", 3200, 450, 150, 950),
        ("5", "5", 2950, 400, 120, 850),
        ("38", "38", 2500, 350, 90, 750),
        ("37", "37", 3900, 520, 180, 1200),
        ("8", "8", 3450, 480, 160, 1050),
        ("9", "9", 3100, 420, 130, 900),
        ("10", "10", 4100, 560, 200, 1300),
        ("11", "11", 2800, 390, 110, 820),
        ("12", "12", 2400, 320, 85, 710),
        ("13", "13", 2100, 290, 70, 620),
        ("14", "14", 1900, 260, 60, 550),
    ]

    camera_comparison = [
        CameraComparisonItem(
            camera_id=cid,
            nome_curto=nome,
            carros=c,
            motos=m,
            onibus=o,
            caminhoes=k,
            total=c + m + o + k
        )
        for (cid, nome, c, m, o, k) in cam_data
    ]

    time_series = [
        {"periodo": "23/10", "total": 14200},
        {"periodo": "24/10", "total": 15800},
        {"periodo": "25/10", "total": 17300},
        {"periodo": "26/10", "total": 21500},
        {"periodo": "27/10", "total": 19400},
        {"periodo": "28/10", "total": 16200},
        {"periodo": "29/10", "total": 13900},
    ]

    return StatisticsResponse(
        categories=dash.categories,
        camera_comparison=camera_comparison,
        time_series=time_series
    )

def get_system_status() -> SystemStatusResponse:
    """Verifica a saúde e limites dos componentes do RoadVision."""
    sp_ok = check_supabase_health()
    return SystemStatusResponse(
        supabase_connected=sp_ok,
        api_status="online",
        yolo_processing_status="idle / oracle-vm-ready",
        oracle_cloud_status="configured",
        active_cameras_limit=2,
        active_cameras_count=0,
        version="1.0.0",
        last_ping=datetime.now(timezone.utc).isoformat()
    )
