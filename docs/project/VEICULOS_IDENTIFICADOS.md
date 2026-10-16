
# Identificação e Rastreamento de Veículos — RoadVision

## 1. Categorias de veículos

| Categoria | Classe no modelo de IA | Necessidade no projeto |
|---|---|---|
| **Carro** | `car` | Identificar e contabilizar veículos de passeio. |
| **Motocicleta** | `motorcycle` | Identificar e contabilizar motos. |
| **Ônibus** | `bus` | Identificar e contabilizar veículos de transporte coletivo. |
| **Caminhão** | `truck` | Identificar e contabilizar veículos de carga. |

## 2. Rastreamento de veículos

O RoadVision utiliza o modelo YOLO integrado ao rastreador ByteTrack para detectar veículos e acompanhar suas posições entre os frames do vídeo.

A implementação está localizada em `src/roadvision/tracking.py`, na classe `VehicleTracker`.

A chamada ao rastreador utiliza `persist=True`, permitindo manter o acompanhamento dos objetos entre frames consecutivos.

O sistema mantém:
- IDs dos veículos observados durante a execução.
- Histórico recente das posições de cada veículo.
- Estados estimados de movimento: `INDEFINIDO`, `PARADO`, `LENTO` e `MOVENDO`.
- IDs ativos no frame mais recente.

## 3. Prevenção de contagens duplicadas

O componente `VehicleCounter`, localizado em `src/roadvision/counter.py`, registra cada ID apenas uma vez.

O método `registrar_cruzamento(track_id, direction)` retorna:
- `True`: quando o ID é contabilizado pela primeira vez.
- `False`: quando o ID já foi contabilizado ou é nulo.

O contador também mantém totais por sentido, permitindo consultar a quantidade de veículos registrada em cada direção.

A classe `LinhaVirtualContagem`, em `src/roadvision/detection/contagem_linha_virtual.py`, identifica os cruzamentos da linha virtual e possui sua própria proteção contra a contagem repetida do mesmo ID.

## 4. Limpeza de dados de rastreamento

O `VehicleTracker` executa verificações periódicas para remover dados auxiliares de veículos inativos.

Configuração padrão:
- **Intervalo de limpeza:** 30 frames.
- **Limite de inatividade:** 300 frames.

Quando um ID permanece inativo pelo limite configurado, o sistema remove sua trajetória, estado confirmado, estado pendente, sequência de confirmação e registro do último frame observado.

O histórico `unique_ids` é preservado durante a execução para manter a quantidade de IDs distintos observados.

O conjunto de IDs contabilizados pelo `VehicleCounter` também é mantido durante a sessão para impedir contagens repetidas.

Esses conjuntos podem crescer ao longo de execuções prolongadas; a limpeza atual limita o crescimento dos dados auxiliares, mas não elimina todo o armazenamento associado aos IDs.

## 5. Testes automatizados

Os testes unitários verificam:
- Contagem única por ID.
- Contagem de veículos diferentes.
- Totais separados por sentido.
- Rejeição de IDs nulos.
- Identificação de cruzamentos e prevenção de duplicações.
- Remoção de dados de rastreamento inativos.
- Preservação dos dados de veículos recentes.
- Preservação do histórico de IDs distintos.

Na validação realizada durante o desenvolvimento da tarefa ROAD-58, foram aprovados 16 testes existentes e 3 testes específicos de limpeza, totalizando 19 testes aprovados.

## 6. Arquivos principais

| Arquivo | Responsabilidade |
|---|---|
| `src/roadvision/tracking.py` | Rastreamento, histórico de posições, estimativa de movimento e limpeza de dados inativos. |
| `src/roadvision/counter.py` | Registro de IDs contabilizados e totais por sentido. |
| `src/roadvision/detection/contagem_linha_virtual.py` | Identificação de cruzamentos e proteção contra contagem repetida. |
| `src/roadvision/capture/captura_video.py` | Integração da captura, rastreamento e contagem no processamento do vídeo. |
| `tests/unit/testar_counter.py` | Testes unitários do contador. |
| `tests/unit/tracking/testar_limpeza_tracking.py` | Testes da limpeza de dados inativos. |
