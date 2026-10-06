# Rastreamento de Veículos — RoadVision

## 1. Objetivo

O módulo de rastreamento do RoadVision tem como objetivo acompanhar individualmente os veículos detectados em frames consecutivos de uma transmissão de vídeo.

Diferentemente da detecção, que identifica a presença de um veículo em um frame específico, o tracking permite manter uma identificação associada ao veículo ao longo de sua passagem pela cena.

Com isso, o sistema consegue:

- identificar individualmente os veículos;
- manter um ID entre frames consecutivos;
- acompanhar o deslocamento do veículo;
- armazenar a trajetória percorrida;
- identificar novos veículos que entram na cena;
- fornecer informações para futuras funcionalidades de contagem e análise de tráfego.

---

# 2. Contexto no RoadVision

O tracking faz parte da etapa de processamento de vídeo e é executado após a detecção dos veículos pelo modelo YOLO.

O fluxo atual pode ser representado da seguinte forma:

```text
┌──────────────────────┐
│    Câmera DER/SP     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Stream HLS      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│        OpenCV        │
│  Captura dos frames  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       YOLO11n        │
│ Detecção de veículos │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      ByteTrack       │
│     Rastreamento     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    ID persistente    │
│    por veículo       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Centroide       │
│  posição do veículo  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Histórico da posição │
│      / trajetória     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Análise de deslocamento│
│ contagem / direção   │
└──────────────────────┘
```
