# Captura de Vídeo

## 1. Objetivo

Desenvolver a funcionalidade responsável por obter o vídeo da câmera selecionada e disponibilizá-lo para o processamento do RoadVision.

A funcionalidade será responsável pela conexão com o stream de vídeo da câmera e pela obtenção dos frames que serão utilizados pelas etapas posteriores do sistema.

## 2. Contexto

O RoadVision utiliza imagens provenientes das câmeras disponibilizadas pelo DER/SP para realizar a identificação e análise dos veículos.

Nesta etapa do desenvolvimento, será implementado o módulo responsável pela captura do vídeo da câmera selecionada.

A captura deverá funcionar de forma independente das etapas de detecção, rastreamento, contagem e identificação de direção dos veículos.

## 3. Fluxo da funcionalidade

```text
Câmera selecionada
       ↓
Identificação da câmera
       ↓
URL do stream
       ↓
Conexão com o vídeo
       ↓
Captura dos frames
       ↓
Disponibilização para o processamento
```

## 4. Responsabilidades

O módulo de captura deverá:

* Receber a identificação da câmera selecionada.
* Obter as informações necessárias para acessar o stream.
* Estabelecer conexão com o vídeo.
* Capturar os frames do stream.
* Disponibilizar os frames para as etapas de processamento.
* Identificar falhas na conexão ou leitura do vídeo.
* Encerrar corretamente a conexão com a câmera.

## 5. Fora do escopo

Nesta etapa, não serão implementadas:

* Detecção de veículos com YOLO.
* Rastreamento dos veículos.
* Definição da direção dos veículos.
* Contagem dos veículos.
* Aplicação das regiões de interesse (ROI).
* Processamento ou armazenamento dos resultados.

Essas funcionalidades serão desenvolvidas em etapas posteriores.

## 6. Tecnologias

A implementação utilizará principalmente:

* Python
* OpenCV
* Stream de vídeo HLS disponibilizado pelas câmeras do DER/SP

## 7. Critérios de aceitação

A funcionalidade será considerada concluída quando:

* For possível selecionar uma câmera.
* O sistema conseguir obter o stream correspondente à câmera selecionada.
* O vídeo puder ser acessado pelo sistema.
* Os frames puderem ser disponibilizados para o processamento do RoadVision.
* O sistema tratar uma falha de conexão ou leitura do stream.
* A conexão puder ser encerrada corretamente.

## 8. Estrutura prevista

```text
src/
└── roadvision/
    ├── capture/
        ├── captura_video.py
    └── ...
```

O código responsável pela captura será desenvolvido nesta mesma estrutura, mantendo a funcionalidade de captura separada das demais etapas do processamento do RoadVision.

## 9. Integração futura

Após a implementação da captura, os frames obtidos serão utilizados pelas etapas seguintes do pipeline do RoadVision:

```text
Captura
   ↓
Processamento
   ↓
Detecção de veículos
   ↓
Rastreamento
   ↓
Direção
   ↓
Contagem
```


# Testes da Captura de Vídeo

## 1. Objetivo

Validar a capacidade do RoadVision de estabelecer conexão com o stream de vídeo de uma câmera do DER/SP e realizar a captura contínua dos frames utilizando Python e OpenCV.

---

## 2. Câmera utilizada no teste

Para a validação inicial foi utilizada a câmera:

- **ID:** 36
- **KM:** 055+000
- **Nome:** KM 055+000 - Maranduba
- **Stream:** `http://200.144.30.103:8084/hls/cam_36/stream.m3u8`

---

## 3. Tecnologias utilizadas

- Python
- OpenCV
- FFmpeg
- Stream HLS (`.m3u8`)

---

## 4. Implementação

Foi criado o arquivo:

`src/roadvision/capture/captura_video.py`

A implementação utiliza o `cv2.VideoCapture()` para estabelecer a conexão com o stream da câmera.

Foi definido explicitamente o backend FFmpeg:

```python
captura = cv2.VideoCapture(STREAM_URL, cv2.CAP_FFMPEG)
```
