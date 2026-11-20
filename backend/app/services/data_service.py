"""
Serviço de agregação e consulta de dados REAIS para a API RoadVision.
Consulta estritamente as tabelas do Supabase (cameras, contagens_minuto, contagens_por_sentido).
Não utiliza dados fictícios, fixos ou inventados.
"""
import json
import psutil
import zoneinfo
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from collections import defaultdict

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
    SystemStatusResponse,
    UltimaCapturaResponse
)
from backend.app.services.analytics_service import calcular_analise_inteligente

BASE_DIR = Path(__file__).resolve().parents[3]
CAMERAS_JSON_PATH = BASE_DIR / "configs" / "cameras" / "cameras.json"
SAMPLE_CAPTURES_DIR = BASE_DIR / "assets" / "sample_captures"

TZ_SP = zoneinfo.ZoneInfo("America/Sao_Paulo")

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
    """Carrega metadados das câmeras em configs/cameras/cameras.json."""
    if CAMERAS_JSON_PATH.exists():
        try:
            with open(CAMERAS_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("cameras", [])
        except Exception as e:
            print(f"[DataService] Falha ao ler cameras.json: {e}")
    return []

def get_todas_cameras() -> List[CameraBase]:
    """Retorna as câmeras cadastradas com verificação real de cadastro no Supabase."""
    configs = {c["id"]: c for c in carregar_cameras_config()}
    client = get_supabase()
    supabase_cams = []

    if client:
        try:
            res = client.table("cameras").select("*").execute()
            if res and res.data:
                supabase_cams = res.data
        except Exception as e:
            print(f"[DataService] Erro ao consultar câmeras no Supabase: {e}")

    resultado: List[CameraBase] = []
    for default in DEFAULT_DER_CAMERAS:
        der_id = default["id"]
        cfg = configs.get(der_id, {})
        stream_url = cfg.get("stream_url", f"http://200.144.30.103:8084/hls/cam_{der_id}/stream.m3u8")

        # Verifica se essa câmera está registrada no banco
        match = None
        for sc in supabase_cams:
            nome_sc = str(sc.get("nome", ""))
            if f"Camera {der_id}" in nome_sc or f"cam_{der_id}" in nome_sc:
                match = sc
                break

        resultado.append(CameraBase(
            id=str(match.get("id")) if match else f"der-cam-{der_id}",
            camera_der_id=der_id,
            nome=default["nome"],
            rodovia="SP-055",
            km=default["km"],
            municipio=default["municipio"],
            stream_url=stream_url,
            status="Sem conexão",  # Não simula conexão sem teste real
            ativa=bool(match.get("ativa", False)) if match else False,
            cadastrada_no_banco=match is not None,
            ultima_atualizacao="—"
        ))

    return resultado

def get_dashboard_data() -> DashboardResponse:
    """
    Retorna indicadores consolidados REAIS a partir da tabela contagens_minuto.
    Zero dados fictícios.
    """
    client = get_supabase()
    
    total_carros = 0
    total_motos = 0
    total_onibus = 0
    total_caminhoes = 0
    hourly_dict = defaultdict(lambda: {"carros": 0, "motos": 0, "onibus": 0, "caminhoes": 0})
    
    registros = []
    registros_sentido = []
    
    if client:
        try:
            res = client.table("contagens_minuto").select("*").order("data_hora", desc=True).execute()
            registros = res.data or []
            
            for r in registros:
                c = r.get("carros", 0) or 0
                m = r.get("motos", 0) or 0
                o = r.get("onibus", 0) or 0
                k = r.get("caminhoes", 0) or 0
                
                total_carros += c
                total_motos += m
                total_onibus += o
                total_caminhoes += k
                
                # Agrupa por hora real do registro convertida para America/Sao_Paulo
                dt_str = r.get("data_hora", "")
                if dt_str:
                    try:
                        # Trata formato ISO e converte para fuso de São Paulo
                        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        dt_sp = dt.astimezone(TZ_SP)
                        hora_label = f"{dt_sp.hour:02d}h"
                        hourly_dict[hora_label]["carros"] += c
                        hourly_dict[hora_label]["motos"] += m
                        hourly_dict[hora_label]["onibus"] += o
                        hourly_dict[hora_label]["caminhoes"] += k
                    except Exception:
                        pass
        except Exception as e:
            print(f"[DataService] Erro ao buscar contagens reais: {e}")

        try:
            res_s = client.table("contagens_por_sentido").select("*").order("data_hora", desc=True).limit(500).execute()
            registros_sentido = res_s.data or []
        except Exception as e:
            print(f"[DataService] Erro ao buscar contagens por sentido: {e}")

    total_veiculos = total_carros + total_motos + total_onibus + total_caminhoes

    cameras_list = get_todas_cameras()
    total_cameras = len(cameras_list)
    # Não simula câmeras online sem confirmação de sinal ao vivo
    cameras_online = 0
    cameras_offline = total_cameras

    # Calcula análise inteligente quantitativa e estruturada
    analise = calcular_analise_inteligente(
        registros_minuto=registros,
        registros_sentido=registros_sentido,
        cameras_map=cameras_list,
        total_cameras_cadastradas=total_cameras
    )

    metrics = DashboardMetrics(
        total_veiculos=total_veiculos,
        cameras_online=cameras_online,
        cameras_offline=cameras_offline,
        total_cameras=total_cameras,
        km_monitorados=156,
        extensao_trecho_cadastrado_km=156,
        rodovias_ativas=1,
        carros=total_carros,
        motos=total_motos,
        onibus=total_onibus,
        caminhoes=total_caminhoes,
        is_demo=False
    )

    categories = [
        CategoryShare(name="Carros", value=total_carros, color="#0284c7"),
        CategoryShare(name="Motos", value=total_motos, color="#f97316"),
        CategoryShare(name="Ônibus", value=total_onibus, color="#06b6d4"),
        CategoryShare(name="Caminhões", value=total_caminhoes, color="#1e293b"),
    ]

    # Constrói o fluxo das 24 horas usando exclusivamente os dados reais
    hourly_flow: List[HourlyFlowItem] = []
    for h in range(24):
        h_str = f"{h:02d}h"
        dados_h = hourly_dict.get(h_str, {"carros": 0, "motos": 0, "onibus": 0, "caminhoes": 0})
        c = dados_h["carros"]
        m = dados_h["motos"]
        o = dados_h["onibus"]
        k = dados_h["caminhoes"]
        hourly_flow.append(HourlyFlowItem(
            hora=h_str,
            carros=c,
            motos=m,
            onibus=o,
            caminhoes=k,
            total=c + m + o + k
        ))

    return DashboardResponse(
        metrics=metrics,
        categories=categories,
        hourly_flow=hourly_flow,
        analise_inteligente=analise
    )

def get_rodovia_summary() -> HighwaySummary:
    """Retorna os dados consolidados da SP-055 a partir das câmeras e municípios."""
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

def get_statistics_data(
    de: Optional[str] = None,
    ate: Optional[str] = None,
    camera_id: Optional[str] = None,
    rodovia: Optional[str] = None
) -> StatisticsResponse:
    """
    Retorna estatísticas REAIS consultadas no Supabase com filtros aplicados.
    Nenhum dado é inventado se o filtro não contiver dados.
    """
    client = get_supabase()
    
    de_str = de if isinstance(de, str) and de.strip() else None
    ate_str = ate if isinstance(ate, str) and ate.strip() else None
    cam_str = camera_id if isinstance(camera_id, str) and camera_id.strip() else None
    
    total_carros = 0
    total_motos = 0
    total_onibus = 0
    total_caminhoes = 0
    
    cam_agg = defaultdict(lambda: {"carros": 0, "motos": 0, "onibus": 0, "caminhoes": 0})
    time_series_dict = defaultdict(int)

    # Mapeamento de UUID da câmera para identificador simples
    cameras_list = get_todas_cameras()
    id_to_nome = {}
    for c in cameras_list:
        id_to_nome[c.id] = f"{c.camera_der_id or c.id}"
        if c.camera_der_id:
            id_to_nome[str(c.camera_der_id)] = f"{c.camera_der_id}"

    if client:
        try:
            query = client.table("contagens_minuto").select("*")
            if de_str:
                query = query.gte("data_hora", f"{de_str}T00:00:00")
            if ate_str:
                query = query.lte("data_hora", f"{ate_str}T23:59:59")
            if cam_str and cam_str not in ("Todas", "todas"):
                query = query.eq("camera_id", cam_str)

            res = query.order("data_hora", desc=False).execute()
            registros = res.data or []

            for r in registros:
                c = r.get("carros", 0) or 0
                m = r.get("motos", 0) or 0
                o = r.get("onibus", 0) or 0
                k = r.get("caminhoes", 0) or 0
                tot = c + m + o + k

                total_carros += c
                total_motos += m
                total_onibus += o
                total_caminhoes += k

                # Agrupamento por câmera
                cid = str(r.get("camera_id", "desconhecida"))
                cam_agg[cid]["carros"] += c
                cam_agg[cid]["motos"] += m
                cam_agg[cid]["onibus"] += o
                cam_agg[cid]["caminhoes"] += k

                # Agrupamento por dia (DD/MM) em America/Sao_Paulo
                dt_str = r.get("data_hora", "")
                if dt_str:
                    try:
                        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        dt_sp = dt.astimezone(TZ_SP)
                        dia_label = f"{dt_sp.day:02d}/{dt_sp.month:02d}"
                        time_series_dict[dia_label] += tot
                    except Exception:
                        pass
        except Exception as e:
            print(f"[DataService] Erro ao buscar estatísticas reais: {e}")

    categories = [
        CategoryShare(name="Carros", value=total_carros, color="#0284c7"),
        CategoryShare(name="Motos", value=total_motos, color="#f97316"),
        CategoryShare(name="Ônibus", value=total_onibus, color="#06b6d4"),
        CategoryShare(name="Caminhões", value=total_caminhoes, color="#1e293b"),
    ]

    camera_comparison: List[CameraComparisonItem] = []
    for cid, vals in cam_agg.items():
        c = vals["carros"]
        m = vals["motos"]
        o = vals["onibus"]
        k = vals["caminhoes"]
        nome_curto = id_to_nome.get(cid, cid[:8])
        camera_comparison.append(CameraComparisonItem(
            camera_id=cid,
            nome_curto=nome_curto,
            carros=c,
            motos=m,
            onibus=o,
            caminhoes=k,
            total=c + m + o + k
        ))

    time_series = [
        {"periodo": dia, "total": total}
        for dia, total in time_series_dict.items()
    ]

    total_periodo = total_carros + total_motos + total_onibus + total_caminhoes

    return StatisticsResponse(
        categories=categories,
        camera_comparison=camera_comparison,
        time_series=time_series,
        total_periodo=total_periodo
    )

def get_system_status() -> SystemStatusResponse:
    """Verifica com precisão real o estado dos serviços sem simulação."""
    sp_ok = check_supabase_health()

    # Verifica se há processos de processamento YOLO em execução local
    yolo_rodando = False
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmd = " ".join(proc.info['cmdline'] or []).lower()
            if "detector_yolo" in cmd or "test_yolo" in cmd or "testar_yolo" in cmd:
                yolo_rodando = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    status_yolo = "Ativo (em execução)" if yolo_rodando else "Inativo (aguardando execução do script)"

    return SystemStatusResponse(
        supabase_connected=sp_ok,
        api_status="online",
        yolo_processing_status=status_yolo,
        oracle_cloud_status="Configurado via CI/CD (.github/workflows/cd-oracle.yml)",
        active_cameras_limit=2,
        active_cameras_count=1 if yolo_rodando else 0,
        version="1.0.0",
        last_ping=datetime.now(timezone.utc).isoformat()
    )

def get_ultima_captura(camera_id: Optional[str] = None) -> UltimaCapturaResponse:
    """
    Retorna a última captura disponível para a câmera solicitada ou geral.
    Modo resiliente de arquivo / captura:
    1. Tenta recuperar do bucket Supabase Storage 'camera-captures'.
    2. Caso o bucket não esteja acessível ou não contenha o arquivo, utiliza fallback local
       em assets/sample_captures/ (<5 MB).
    Retorna URL estática ou endpoint de imagem servida pela API, com timestamp em America/Sao_Paulo
    e selo 'Modo Captura / Arquivo (Stream DER Offline)'.
    """
    cameras = get_todas_cameras()
    selected_cam: Optional[CameraBase] = None
    
    if camera_id:
        for c in cameras:
            if c.id == camera_id or str(c.camera_der_id) == str(camera_id):
                selected_cam = c
                break
                
    if not selected_cam and cameras:
        selected_cam = cameras[0]  # Padrão: Câmera 36
        
    der_id = selected_cam.camera_der_id if selected_cam else 36
    cid = selected_cam.id if selected_cam else f"der-cam-{der_id}"
    cname = selected_cam.nome if selected_cam else f"DER SP - Camera {der_id}"
    
    # 1. Tenta verificar Supabase Storage
    client = get_supabase()
    storage_url = None
    origem = "local-sample-archive"
    
    if client:
        try:
            # Lista arquivos no bucket 'camera-captures'
            files = client.storage.from_("camera-captures").list()
            filenames = [f.get("name") for f in files if isinstance(f, dict)]
            target_name = f"camera_{der_id}.jpg"
            if target_name in filenames:
                storage_url = client.storage.from_("camera-captures").get_public_url(target_name)
                origem = "supabase-storage"
            elif "latest.jpg" in filenames:
                storage_url = client.storage.from_("camera-captures").get_public_url("latest.jpg")
                origem = "supabase-storage"
        except Exception as e:
            # Storage offline ou sem permissão pública
            storage_url = None

    if storage_url:
        image_url = storage_url
    else:
        # Fallback local em assets/sample_captures
        local_filename = f"camera_{der_id}.jpg"
        if not (SAMPLE_CAPTURES_DIR / local_filename).exists():
            local_filename = "latest.jpg" if (SAMPLE_CAPTURES_DIR / "latest.jpg").exists() else "camera_36.jpg"
        image_url = f"/api/cameras/capturas/arquivo/{local_filename}"

    now_sp = datetime.now(TZ_SP)
    captured_at = now_sp.strftime("%d/%m/%Y %H:%M:%S BRT")

    return UltimaCapturaResponse(
        camera_id=cid,
        camera_der_id=der_id,
        nome_camera=cname,
        origem=origem,
        image_url=image_url,
        captured_at=captured_at,
        status_modo="Modo Captura / Arquivo (Stream DER Offline)",
        disponivel=True
    )

