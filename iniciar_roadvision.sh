#!/usr/bin/env bash
# ===============================================================================
#                     ROADVISION — MONITORAMENTO INTELIGENTE
#                   DER/SP • SP-055 RIO-SANTOS • IA YOLO & FASTAPI
# ===============================================================================

set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "==============================================================================="
echo "                     ROADVISION — MONITORAMENTO INTELIGENTE"
echo "==============================================================================="

# Detecção do binário Python
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
else
    echo "Erro: Python 3 não encontrado no PATH."
    exit 1
fi

echo "[1/4] Iniciando Backend FastAPI na porta 8000..."
$PY_CMD -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

echo "[2/4] Iniciando Frontend React na porta 5173..."
cd "$PROJECT_ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo "[3/4] Aguardando 5 segundos para inicialização dos serviços..."
sleep 5

echo "[4/4] Abrindo navegador em http://localhost:5173..."
if command -v xdg-open &>/dev/null; then
    xdg-open "http://localhost:5173" &>/dev/null || true
elif command -v open &>/dev/null; then
    open "http://localhost:5173" || true
fi

echo ""
echo "==============================================================================="
echo " RoadVision ativo!"
echo " -> Frontend: http://localhost:5173"
echo " -> Swagger API: http://localhost:8000/docs"
echo " Pressione Ctrl+C para encerrar os servidores."
echo "==============================================================================="

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM
wait
