
# Integração do Modelo YOLO

## 1. Objetivo

Integrar o modelo YOLO ao RoadVision para realizar a detecção automática de veículos nos frames provenientes das câmeras do DER/SP.

A integração permite que os frames capturados sejam enviados para o modelo de inteligência artificial, que identifica veículos e retorna as detecções para posterior utilização no rastreamento e na contagem de veículos.

---

## 2. Modelo utilizado

O RoadVision utiliza o modelo:

- **Modelo:** YOLO11n
- **Framework:** Ultralytics
- **Arquivo dos pesos:** `models/yolo11n.pt`
- **Versão do Ultralytics:** `8.4.131`

O modelo foi escolhido por apresentar um bom equilíbrio entre velocidade de processamento e capacidade de detecção, sendo adequado para uma aplicação de monitoramento de vídeo.

---

## 3. Estrutura implementada

A lógica de detecção foi centralizada em:

```text
src/
└── roadvision/
    ├── capture/
    │   └── captura_video.py
    │
    └── detection/
        └── detector_yolo.py
```
