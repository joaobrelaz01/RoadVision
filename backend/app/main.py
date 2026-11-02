"""
Ponto de entrada da API RoadVision FastAPI.
Mantém intactos o processamento YOLO, o código Python existente e a conexão Supabase.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import CORS_ORIGINS
from backend.app.routes import (
    dashboard,
    cameras,
    contagens,
    estatisticas,
    relatorios,
    status,
    auth
)

app = FastAPI(
    title="RoadVision API",
    description="API de monitoramento inteligente de rodovias com IA YOLO e Supabase.",
    version="1.0.0"
)

# Configuração de CORS para permitir requisições do frontend React / Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas modulares
app.include_router(dashboard.router)
app.include_router(cameras.router)
app.include_router(contagens.router)
app.include_router(estatisticas.router)
app.include_router(relatorios.router)
app.include_router(status.router)
app.include_router(auth.router)

@app.get("/")
def raiz():
    return {
        "sistema": "RoadVision API",
        "versao": "1.0.0",
        "status": "operacional",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
