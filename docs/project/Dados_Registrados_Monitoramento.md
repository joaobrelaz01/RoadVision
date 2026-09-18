
# Dados Registrados Durante o Monitoramento — RoadVision

## 1. Objetivo

Definir quais informações deverão ser registradas pelo RoadVision durante o monitoramento das rodovias, permitindo organizar e armazenar os dados relacionados aos veículos identificados pelas câmeras.

## 2. Dados coletados

Durante o monitoramento, o RoadVision deverá registrar as seguintes informações:

| Dado                    | Descrição                                                                                                                                         |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tipo de veículo        | Classificação do veículo identificado, como carro, caminhão, ônibus ou motocicleta.                                                            |
| Sentido                 | Direção em que o veículo está se deslocando, conforme o sentido identificado na rodovia.                                                        |
| Data                    | Data em que o veículo foi identificado.                                                                                                            |
| Horário                | Horário em que o veículo foi identificado durante o monitoramento.                                                                                |
| Câmera                 | Identificação da câmera responsável pela captura do veículo.                                                                                   |
| Quantidade de veículos | Quantidade de veículos identificados no período de monitoramento, podendo ser organizada por câmera, tipo de veículo, sentido, data e horário. |

## 3. Estrutura das informações

Os dados coletados deverão permitir a organização das informações de forma estruturada, possibilitando posteriormente sua utilização para armazenamento, consultas, geração de indicadores e visualização no dashboard do RoadVision.

A estrutura deverá relacionar cada registro de monitoramento à câmera utilizada e ao momento em que a identificação ocorreu.

Exemplo conceitual:

```text
Registro de monitoramento
├── Câmera
├── Data
├── Horário
├── Tipo de veículo
├── Sentido
└── Quantidade
```
