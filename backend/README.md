# 🚗 RoadVision — Backend API (FastAPI)

API REST desenvolvida em FastAPI para conectar o frontend React aos dados do Supabase e ao processamento de Inteligência Artificial do RoadVision.

---

## 📌 Rotas da API

- `GET /api/dashboard`: Retorna indicadores e gráficos consolidados das últimas 24h.
- `GET /api/cameras`: Lista as 11 câmeras do DER/SP na SP-055.
- `GET /api/cameras/{id}`: Detalhes de uma câmera individual.
- `GET /api/rodovias`: Resumo dos trechos e municípios da SP-055.
- `GET /api/contagens`: Consulta contagens históricas por minuto (`contagens_minuto`).
- `GET /api/contagens/por-sentido`: Consulta contagens separadas por sentido (`contagens_por_sentido` — Maranduba / Ubatuba).
- `GET /api/estatisticas`: Dados analíticos e comparações entre câmeras.
- `GET /api/relatorios`: Dados tabulares para geração de relatórios.
- `GET /api/status`: Diagnóstico e saúde dos serviços (Supabase, API, Oracle VM).
- `POST /api/auth/login`: Autenticação e emissão de token.
- `GET /api/auth/usuarios`: Listagem de usuários autorizados.

---

## 🚀 Como Executar o Backend

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

A documentação interativa Swagger estará disponível em: `http://localhost:8000/docs`
