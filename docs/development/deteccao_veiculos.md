
# Detecção de Veículos com YOLO — RoadVision

## 1. Objetivo

Implementar a primeira detecção de veículos em imagens utilizando o modelo YOLO pré-treinado, permitindo validar a identificação de objetos e a posição das caixas de detecção.

## 2. Requisitos

- Python e ambiente virtual do projeto `.venv`.
- Dependências instaladas a partir de `requirements.txt`.
- Pesos do modelo disponíveis em `models/yolo11n.pt`.
- Uma imagem de teste em formato JPG, JPEG, PNG, BMP ou WEBP.

## 3. Arquivos envolvidos

- `src/roadvision/detection/deteccao_veiculos.py`: script de execução da detecção.
- `src/roadvision/detection/detector_yolo.py`: carregamento do modelo e implementação existente do detector.
- `models/yolo11n.pt`: pesos do modelo YOLO.
- `tests/frames/`: frames capturados utilizados para testes.
- `data/resultados/`: imagens geradas com as caixas de detecção.

## 4. Preparação do ambiente

Ative o ambiente virtual e configure o caminho do pacote no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\src"
```

As dependências devem estar instaladas conforme o arquivo `requirements.txt`.

## 5. Executar a detecção

Para processar um frame já capturado:

```powershell
python src\roadvision\detection\deteccao_veiculos.py tests\frames\frame_4.jpg
```

Para processar imagens encontradas em `data/`, execute:

```powershell
python src\roadvision\detection\deteccao_veiculos.py
```

O script utiliza o modelo YOLO e filtra as classes carro, moto e caminhão.

## 6. Resultados

O script apresenta no terminal:

- Quantidade de objetos detectados.
- Classe identificada.
- Confiança estimada pelo modelo.
- Coordenadas das caixas delimitadoras.

A imagem anotada é salva na pasta `data/resultados/` e exibida em uma janela para inspeção visual.

Exemplo de saída gerada no teste com `frame_4.jpg`:

- Modelo carregado: `models/yolo11n.pt`.
- Veículos detectados: 3.
- Classes retornadas: carro.
- Confianças registradas: aproximadamente 34,43%, 30,59% e 26,68%.

Esses valores representam o resultado observado naquele frame e não garantem a mesma quantidade ou confiança em outras imagens.

## 7. Validação

A compilação do módulo pode ser verificada com:

```powershell
python -m compileall src\roadvision\detection
```

A validação funcional deve incluir:

1. Confirmar que o modelo é carregado sem erros.
2. Executar a detecção em uma imagem real.
3. Verificar se as caixas delimitadoras estão posicionadas sobre veículos.
4. Conferir a imagem gerada em `data/resultados/`.

A detecção técnica foi executada com sucesso em `tests/frames/frame_4.jpg`. A precisão das classificações e o posicionamento de cada caixa devem ser avaliados visualmente, especialmente em imagens noturnas.

## 8. Observações

O modelo utilizado é o YOLO11n pré-treinado. O script filtra carros, motos e caminhões. A classe ônibus existe no detector compartilhado, mas não faz parte do filtro específico desta execução.
