
# Relatório de Testes — Rastreamento de Veículos

**Projeto:** RoadVision
**Task Jira:** ROAD-52 — Testar rastreamento em vídeo
**Área:** Visão Computacional / Rastreamento
**Data do teste:** 13/10/2026
**Status:** Execução completa; validação visual detalhada pendente.

## 1. Objetivo

Validar o funcionamento do rastreamento de veículos em uma gravação real de câmera do DER/SP, verificando a integração entre YOLO e ByteTrack, a geração de IDs, as trajetórias e os estados estimados de movimento.

## 2. Ambiente e configuração

- Fonte: câmera 14 do DER/SP.
- Entrada: vídeo gravado da transmissão real.
- Arquivo: `data/videos/der_cam_14.mp4`.
- Modelo: `models/yolo11n.pt`.
- Rastreador: ByteTrack, utilizando `persist=True`.
- Classes avaliadas: carro, moto, ônibus e caminhão.
- Implementação: `src/roadvision/tracking.py`.
- Script de teste: `tests/manual/tracking/testar_tracking_video.py`.

## 3. Resultados obtidos

| Métrica                            | Resultado |
| ----------------------------------- | --------: |
| Frames gravados                     |     2.156 |
| Frames processados                  |     2.156 |
| IDs distintos observados            |        33 |
| FPS médio de processamento         |      8,56 |
| Ausências temporárias registradas |        18 |
| Frames com IDs duplicados           |         0 |

## 4. Arquivos gerados

- Vídeo anotado: `data/resultados/tracking/der_cam_14_tracking.mp4`
- Relatório de métricas: `data/resultados/tracking/der_cam_14_relatorio.json`

O vídeo processado apresenta as caixas delimitadoras, os IDs atribuídos aos veículos, suas trajetórias registradas e os estados estimados de movimento.

## 5. Análise dos resultados

O processamento integral foi concluído e gerou os arquivos esperados. O sistema detectou veículos e apresentou os estados de movimento implementados no projeto.

Nenhum frame com IDs duplicados foi registrado pelo verificador do teste. Esse resultado se refere à duplicação do mesmo ID dentro de um único frame e não comprova, isoladamente, a identidade correta de todos os veículos.

Foram registradas 18 ausências temporárias de IDs. Esses eventos precisam ser examinados no vídeo para distinguir oclusões, falhas momentâneas de detecção e possíveis perdas de rastreamento.

Os 33 IDs representam identificações distintas observadas durante a execução e não equivalem necessariamente à quantidade real de veículos que passaram pela câmera.

## 6. Validações pendentes

- [ ] Conferir visualmente se os IDs permanecem consistentes durante o deslocamento.
- [ ] Examinar os 18 eventos de ausência temporária.
- [ ] Verificar situações de sobreposição e oclusão.
- [ ] Confirmar se novos veículos recebem IDs adequados.
- [ ] Repetir os testes com outras condições de tráfego e iluminação.

## 7. Conclusão

O teste técnico foi executado com sucesso sobre 2.156 frames de uma gravação real do DER/SP, com geração de vídeo anotado e relatório de métricas.

Os resultados iniciais indicam que a integração de detecção e rastreamento está operacional. Entretanto, a consistência dos IDs ao longo de toda a trajetória e o comportamento em situações de oclusão ainda dependem de revisão visual e testes adicionais.

A task deverá ser considerada plenamente validada após a análise dos eventos registrados e a documentação das evidências observadas.
