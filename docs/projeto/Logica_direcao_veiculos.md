
# Task 13 — Definir como será identificada a direção dos veículos

## Objetivo

Definir a lógica que será utilizada pelo RoadVision para identificar a direção de deslocamento dos veículos detectados pelas câmeras rodoviárias.

## Lógica definida

A direção dos veículos será identificada por meio do acompanhamento da trajetória de cada veículo ao longo dos frames do vídeo.

O YOLO será responsável pela detecção dos veículos presentes na imagem. Após a detecção, cada veículo deverá ser acompanhado por um mecanismo de rastreamento, permitindo analisar sua movimentação entre diferentes frames.

A direção será determinada a partir da variação da posição do veículo ao longo do tempo. Dessa forma, será possível identificar se o veículo está se deslocando em uma direção ou na direção oposta.

## Definição dos sentidos

Para cada câmera, serão definidos dois sentidos de deslocamento:

* **Sentido 1:** direção principal definida para a câmera;
* **Sentido 2:** direção oposta ao Sentido 1.

A identificação de qual direção corresponde a cada sentido será configurada individualmente para cada câmera, considerando sua posição, orientação e o sentido real da rodovia.

## Fluxo definido

1. Captura do frame da câmera;
2. Detecção dos veículos utilizando YOLO;
3. Rastreamento dos veículos entre os frames;
4. Identificação da posição do veículo;
5. Análise da movimentação do veículo;
6. Classificação da direção como Sentido 1 ou Sentido 2.

## Resultado

Foi definida a utilização da trajetória dos veículos como base para identificação da direção de deslocamento. A solução permitirá que cada câmera possua seus próprios sentidos configurados de acordo com a orientação da rodovia.

A presente tarefa corresponde à definição da lógica. A implementação do mecanismo de detecção, rastreamento e classificação será realizada em tarefas posteriores.
