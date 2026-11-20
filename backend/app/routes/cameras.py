from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from typing import List, Optional
from pathlib import Path
import cv2
import time
import requests

from backend.app.schemas.models import CameraBase, HighwaySummary, UltimaCapturaResponse
from backend.app.services.data_service import (
    get_todas_cameras,
    get_rodovia_summary,
    get_ultima_captura,
    SAMPLE_CAPTURES_DIR
)

router = APIRouter(prefix="/api", tags=["Câmeras e Rodovias"])

@router.get("/cameras", response_model=List[CameraBase])
def listar_cameras():
    """Lista todas as 11 câmeras cadastradas da SP-055 com seus status e metadados."""
    return get_todas_cameras()

@router.get("/cameras/ultima-captura", response_model=UltimaCapturaResponse)
def obter_ultima_captura_geral():
    """Retorna a última captura disponível da rodovia (padrão Câmera 36 ou mais recente)."""
    return get_ultima_captura(None)

@router.get("/cameras/capturas/arquivo/{filename}")
def servir_arquivo_captura(filename: str):
    """Serve a imagem de captura estática do repositório local em fallback resiliente."""
    # Sanitiza o nome do arquivo para evitar Path Traversal
    safe_name = Path(filename).name
    file_path = SAMPLE_CAPTURES_DIR / safe_name
    if not file_path.exists() or not file_path.is_file():
        # Fallback para latest.jpg ou camera_36.jpg
        fallback_path = SAMPLE_CAPTURES_DIR / "latest.jpg"
        if fallback_path.exists():
            file_path = fallback_path
        else:
            raise HTTPException(status_code=404, detail="Arquivo de captura não encontrado")
    return FileResponse(file_path, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=30"})

@router.get("/cameras/{camera_id}/live/status")
def status_stream_ao_vivo(camera_id: str):
    """Verifica se o stream HLS da câmera responde com playlist m3u8 válida do DER/SP."""
    cameras = get_todas_cameras()
    target_cam = next((c for c in cameras if c.id == camera_id or str(c.camera_der_id) == str(camera_id)), None)
    der_id = target_cam.camera_der_id if target_cam else camera_id
    stream_url = target_cam.stream_url if target_cam and target_cam.stream_url else f"http://200.144.30.103:8084/hls/cam_{der_id}/stream.m3u8"

    try:
        r = requests.get(stream_url, timeout=3)
        ativo = r.status_code == 200 and "#EXTM3U" in r.text
        return {
            "camera_id": camera_id,
            "stream_url": stream_url,
            "disponivel": ativo,
            "status_code": r.status_code
        }
    except Exception as e:
        return {
            "camera_id": camera_id,
            "stream_url": stream_url,
            "disponivel": False,
            "erro": str(e)
        }

@router.get("/cameras/{camera_id}/live")
def obter_stream_ao_vivo(camera_id: str):
    """
    Abre o stream ao vivo real das câmeras DER/SP via OpenCV CAP_FFMPEG e entrega
    em tempo real via StreamingResponse MJPEG (multipart/x-mixed-replace),
    sem bloqueio de CORS ou Referer no navegador.
    """
    cameras = get_todas_cameras()
    target_cam = next((c for c in cameras if c.id == camera_id or str(c.camera_der_id) == str(camera_id)), None)
    der_id = target_cam.camera_der_id if target_cam else camera_id
    stream_url = target_cam.stream_url if target_cam and target_cam.stream_url else f"http://200.144.30.103:8084/hls/cam_{der_id}/stream.m3u8"

    def gerar_frames():
        cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Se falhar ao abrir a conexão direta com o stream
        if not cap.isOpened():
            # Fallback para frame de segurança da câmera se o stream DER estiver offline
            local_fallback = SAMPLE_CAPTURES_DIR / f"camera_{der_id}.jpg"
            if not local_fallback.exists():
                local_fallback = SAMPLE_CAPTURES_DIR / "latest.jpg"
            if local_fallback.exists():
                with open(local_fallback, "rb") as f:
                    fb_bytes = f.read()
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + fb_bytes + b'\r\n'
                )
            cap.release()
            return

        try:
            tentativas_vazias = 0
            while True:
                sucesso, frame = cap.read()
                if not sucesso or frame is None:
                    tentativas_vazias += 1
                    time.sleep(0.05)
                    if tentativas_vazias > 20:
                        break
                    continue

                tentativas_vazias = 0
                ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
                if not ret:
                    continue

                frame_bytes = buffer.tobytes()
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
                )
                time.sleep(0.04)  # ~25 FPS
        except GeneratorExit:
            pass
        finally:
            cap.release()

    return StreamingResponse(
        gerar_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Access-Control-Allow-Origin": "*"
        }
    )

@router.get("/cameras/{camera_id}/ultima-captura", response_model=UltimaCapturaResponse)
def obter_ultima_captura_camera(camera_id: str):
    """Retorna a última captura disponível para uma câmera específica."""
    return get_ultima_captura(camera_id)

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

