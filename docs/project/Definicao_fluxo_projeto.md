
# Fluxo Geral do Sistema — RoadVision

## 1. Objetivo

O RoadVision é um sistema destinado ao monitoramento e análise do fluxo de veículos em rodovias por meio de imagens provenientes de câmeras públicas do DER/SP.

O sistema realiza a seleção das câmeras, captura dos frames, processamento das imagens por visão computacional, detecção e rastreamento dos veículos, contagem dos veículos identificados, armazenamento dos resultados e disponibilização das informações para visualização.

---

## 2. Fluxo geral

O funcionamento do RoadVision pode ser representado pelas seguintes etapas:

```text
Câmeras DER/SP
      ↓
Seleção da câmera
      ↓
Captura da transmissão
      ↓
Extração dos frames
      ↓
Processamento da imagem
      ↓
Detecção dos veículos
      ↓
Rastreamento dos veículos
      ↓
Contagem e classificação
      ↓
Armazenamento dos dados
      ↓
Dashboard / Visualização
```

![1789150906657](image/Definicao_fluxo_projeto/1789150906657.png)
