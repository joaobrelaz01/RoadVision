# 🚗 RoadVision — Frontend Web

Frontend moderno e responsivo do sistema **RoadVision**, construído com React, TypeScript, Vite, Tailwind CSS, Lucide React e Recharts, reproduzindo com fidelidade a identidade visual oficial.

---

## 📌 Funcionalidades

O sistema conta com as 8 páginas completas:
1. **Dashboard:** Métricas consolidadas (Total de veículos 47.152, Carros, Motos, Ônibus, Caminhões), gráficos em Donut e curvas horárias de fluxo (Spline).
2. **Monitoramento ao Vivo:** Visualização de streams HLS (`.m3u8`) com `hls.js`, lista das 11 câmeras do DER/SP e limite operacional estrito de até 2 câmeras simultâneas.
3. **Rodovias:** Detalhamento da rodovia SP-055 (Rio-Santos), trechos monitorados e status por município (Maranduba, Caraguatatuba, São Sebastião, Massaguaçu, Bertioga).
4. **Câmeras:** Tabela completa com pesquisa em tempo real e filtros por município e status.
5. **Estatísticas:** Filtros temporais, gráficos comparativos empilhados entre as câmeras e evolução no tempo.
6. **Relatórios:** Consultas históricas, métricas por categoria e sentido (Maranduba / Ubatuba), com exportação funcional para **Excel (.xlsx)** e **PDF**.
7. **Usuários:** Controle de permissões (Administrador, Operador, Visualizador), controle de status e cadastro de novos operadores.
8. **Configurações:** Monitoramento do estado do banco Supabase, backend FastAPI, modelo YOLO11 e parâmetros de infraestrutura na Oracle Cloud.

---

## 🚀 Como Executar

### 1. Pré-requisitos
- Node.js instalado (v26+ ou LTS)
- Dependências instaladas (`npm install`)

### 2. Rodar em Modo de Desenvolvimento
```bash
cd frontend
npm run dev
```
O frontend estará acessível em: `http://localhost:5173`

### 3. Gerar Build de Produção
```bash
cd frontend
npm run build
```
Os arquivos otimizados serão gerados na pasta `frontend/dist/`.
