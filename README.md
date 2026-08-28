
# 🚗 RoadVision

Sistema de monitoramento inteligente de rodovias utilizando câmeras do DER, visão computacional e Inteligência Artificial.

## 🎯 Objetivo

Desenvolver um sistema capaz de analisar imagens provenientes de câmeras rodoviárias para:

- Detectar veículos;
- Classificar veículos;
- Contabilizar o fluxo de veículos;
- Identificar o sentido do tráfego;
- Armazenar os dados coletados;
- Disponibilizar informações para análise em dashboard;
- Futuramente identificar padrões de fluxo utilizando IA.

## 🏗️ Arquitetura planejada

Câmeras DER
↓
Captura de frames
↓
Python + OpenCV
↓
YOLO
↓
Detecção e contagem de veículos
↓
API
↓
Banco de dados
↓
Dashboard
↓
Análise histórica e IA

## 🛠️ Tecnologias

- Python 3.12
- OpenCV
- Ultralytics YOLO
- PyTorch
- Playwright
- Git
- GitHub
- VS Code

## 📁 Estrutura do projeto

```text
RoadVision/
├── data/          # Dados utilizados pelo projeto
├── models/        # Modelos de IA
├── src/           # Código principal
├── tests/         # Testes automatizados
├── .gitignore
├── requirements.txt
├── teste.py
└── README.md
```
