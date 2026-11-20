@echo off
chcp 65001 > nul
title RoadVision — Inicializador do Sistema Integrado
cls

echo ===============================================================================
echo                      ROADVISION — MONITORAMENTO INTELIGENTE
echo                    DER/SP • SP-055 RIO-SANTOS • IA YOLO & FASTAPI
echo ===============================================================================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1/4] Verificando dependências Python...
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PY_CMD=py -3.14
) else (
    set PY_CMD=python
)

echo [2/4] Iniciando Backend FastAPI (Porta 8000)...
start "RoadVision - Backend FastAPI" cmd /k "cd /d \"%SCRIPT_DIR%\" && %PY_CMD% -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [3/4] Iniciando Frontend React + Vite (Porta 5173)...
start "RoadVision - Frontend Vite" cmd /k "cd /d \"%SCRIPT_DIR%frontend\" && npm run dev"

echo [4/4] Aguardando inicialização dos serviços (5 segundos)...
timeout /t 5 /nobreak > nul

echo.
echo ===============================================================================
echo  RoadVision pronto para uso!
echo  -> Painel Frontend: http://localhost:5173
echo  -> Documentação Swagger API: http://localhost:8000/docs
echo ===============================================================================
echo.

start http://localhost:5173

echo Pressione qualquer tecla para fechar esta janela (os servidores continuarao rodando).
pause > nul
