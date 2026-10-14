
# Relatório de Avaliação da Precisão das Detecções — RoadVision

**Task:** ROAD-53 — Task 40
**Modelo:** YOLO11n (`models/yolo11n.pt`)
**Vídeo avaliado:** `data/videos/der_cam_14.mp4`
**Câmera:** DER/SP — câmera 14
**Data da avaliação:** 13/10/2026
**Status:** Avaliação preliminar concluída; validação quantitativa pendente.

## 1. Objetivo

Avaliar o comportamento do detector YOLO do RoadVision em vídeo real, identificando possíveis falsos positivos, falsos negativos, erros de classificação e dificuldades de detecção em condições noturnas.

A atividade não contempla retreinamento ou alteração dos pesos do modelo.

## 2. Ambiente e amostragem

Foi utilizado um vídeo previamente gravado da câmera DER/SP.

| Item                             | Resultado                      |
| -------------------------------- | ------------------------------ |
| Arquivo de entrada               | `data/videos/der_cam_14.mp4` |
| Resolução                      | 704 × 480                     |
| FPS original                     | 20                             |
| Frames lidos                     | 2.156                          |
| Intervalo de amostragem          | 2 segundos                     |
| Amostras geradas                 | 54                             |
| Tempo de execução do avaliador | 16,98 segundos                 |
| Modelo                           | `models/yolo11n.pt`          |

O script `tests/manual/detection/avaliar_precisao_deteccao.py` gerou imagens anotadas e o arquivo JSON com as detecções, suas classes, confianças e coordenadas.

## 3. Classes avaliadas

O detector considera as seguintes classes de veículos:

- Carro;
- Moto;
- Ônibus;
- Caminhão.

## 4. Observações da inspeção visual

A inspeção preliminar das imagens indicou:

- Detecções aparentemente corretas de veículos em algumas amostras;
- Confianças relativamente baixas em determinadas detecções;
- Possíveis falsos positivos em regiões com vegetação ou objetos pouco definidos;
- Dificuldade de avaliação de veículos pequenos ou distantes;
- Períodos sem caixas de detecção que precisam ser comparados com os veículos realmente visíveis.

As observações são qualitativas. Os casos suspeitos não foram contabilizados como erros confirmados sem verificação suficiente da imagem original.

## 5. Métricas quantitativas

| Métrica                             | Resultado                 |
| ------------------------------------ | ------------------------- |
| Precisão (precision)                | Não calculada            |
| Recall                               | Não calculado            |
| Taxa de falsos positivos             | Não calculada            |
| Erros de classificação confirmados | Ainda não contabilizados |
| Amostras geradas                     | 54                        |

As métricas quantitativas permanecem pendentes porque ainda é necessário estabelecer uma referência manual confiável, contando os veículos reais em cada amostra e comparando-os com as detecções do modelo.

A quantidade de caixas geradas pelo YOLO não é suficiente para calcular essas métricas.

## 6. Arquivos produzidos

- `tests/manual/detection/avaliar_precisao_deteccao.py` — geração das amostras e do JSON;
- `tests/manual/detection/gerar_folha_revisao.py` — geração da folha visual;
- `data/resultados/detection/avaliacao_precisao.json` — resultados das detecções;
- `data/resultados/detection/amostras/` — imagens individuais;
- `data/resultados/detection/folha_revisao.jpg` — folha de revisão visual.

## 7. Limitações

- A inspeção visual realizada até o momento é preliminar.
- Nem todas as 54 amostras foram validadas individualmente.
- A ausência de detecções não comprova, isoladamente, a existência de falsos negativos.
- Uma caixa desenhada não comprova que a detecção ou a classificação está correta.
- Os resultados se referem a um vídeo noturno de uma única câmera e não representam todas as condições de operação do RoadVision.

## 8. Conclusão

O avaliador foi executado com sucesso, processando 2.156 frames e gerando 54 amostras para inspeção visual. Foram identificados casos que merecem revisão, especialmente detecções com baixa confiança e objetos em regiões que não parecem corresponder claramente a veículos.

A avaliação quantitativa da precisão do modelo ainda não foi concluída. A próxima etapa é finalizar a anotação manual das amostras, confirmar os erros e calcular as métricas a partir dessa referência.

Nenhum retreinamento foi realizado nesta atividade.
