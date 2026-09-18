\# Testes Técnicos — RoadVision



Esta documentação registra os testes realizados durante o desenvolvimento do RoadVision para validar o acesso às câmeras do DER/SP, a obtenção dos streams de vídeo, a captura utilizando OpenCV, a detecção de veículos com YOLO e os primeiros testes de rastreamento e contagem.



Inicialmente, o projeto utilizou o Playwright para acessar o site do DER e localizar automaticamente as câmeras da rodovia SP-055 — Doutor Manoel Hypollito Rego. Foram identificadas 11 câmeras para os testes iniciais: ID 36 — KM 055+000 — sentido MARANDUBA; ID 5 — KM 073+000 — sentido MARANDUBA; ID 38 — KM 083+500 — sentido MARANDUBA; ID 37 — KM 092+500 — sentido CARAGUATATUBA; ID 8 — KM 110+000 — sentido SÃO SEBASTIÃO; ID 9 — KM 110+000 — sentido MASSAGUAÇU; ID 10 — KM 136+000 — sentido CARAGUATATUBA; ID 11 — KM 168+000 — sentido BERTIOGA; ID 12 — KM 193+000 — sentido SÃO SEBASTIÃO; ID 13 — KM 211+000 — sentido SÃO SEBASTIÃO; e ID 14 — KM 211+000 — sentido BERTIOGA.



No primeiro teste, foi utilizado o navegador para selecionar as câmeras e acessar seus respectivos players de vídeo. As 11 câmeras foram encontradas corretamente e os players também foram localizados. Entretanto, o elemento de vídeo apresentava endereços no formato "blob:", como "blob:http://200.144.30.103:8084/...", e esses endereços não puderam ser utilizados diretamente pelo OpenCV. O resultado inicial foi de 11 câmeras encontradas, 11 players encontrados, 11 streams identificados no player e nenhuma câmera acessível diretamente pelo OpenCV através do endereço apresentado pelo navegador.



A partir desse problema, foi realizada uma investigação das requisições realizadas pelo próprio site do DER. Durante essa análise foi encontrada a API de câmeras disponível em "http://200.144.30.103:8084/api/cameras". Essa API retorna informações das câmeras, incluindo ID, rodovia, KM, nome, localização, status, sentido, latitude e longitude. A descoberta dessa API permitiu relacionar diretamente o ID de cada câmera com suas informações e facilitou a identificação das câmeras utilizadas pelo projeto.



Durante a investigação também foi descoberta a forma como os vídeos são transmitidos pelo sistema. As câmeras utilizam streams no formato HLS, disponibilizados através de arquivos ".m3u8". O padrão identificado foi "http://200.144.30.103:8084/hls/cam\_ID/stream.m3u8". Por exemplo, para a câmera de ID 8 foi identificado o endereço "http://200.144.30.103:8084/hls/cam\_8/stream.m3u8". Durante a reprodução também foram observados segmentos de vídeo no formato ".ts", como "stream10.ts", "stream11.ts", "stream12.ts", "stream13.ts" e "stream14.ts".



Depois da descoberta dos streams HLS, foi criado um teste para verificar automaticamente as 11 câmeras. O resultado foi positivo: foram testados 11 streams e os 11 foram considerados funcionando. Dessa forma, foi possível confirmar que as câmeras selecionadas da SP-055 possuíam streams HLS acessíveis durante os testes.



Em seguida, foi realizado um teste utilizando o OpenCV diretamente nos streams HLS. O objetivo era verificar se o Python conseguiria capturar frames sem utilizar o navegador. O resultado também foi positivo: as 11 câmeras testadas conseguiram fornecer frames através do OpenCV. Esse teste foi importante porque demonstrou que não seria necessário manter o navegador aberto para realizar a captura dos vídeos.



Após validar a captura dos frames, foi integrado o modelo YOLO utilizando o arquivo "yolo11n.pt". O primeiro teste de detecção foi realizado com uma das câmeras da SP-055 e o modelo conseguiu identificar os objetos presentes na imagem, apresentando as caixas de detecção sobre os veículos e outros objetos reconhecidos. Durante esse teste foi observado que o YOLO também poderia detectar objetos que estavam fora da área principal da rodovia. Essa situação não foi tratada neste momento, pois posteriormente será necessário definir uma região de interesse (ROI) para determinar exatamente qual parte da imagem deverá ser analisada.



Também foi realizado um teste utilizando a câmera ID 14, localizada no KM 211+000, sentido BERTIOGA, escolhida por apresentar maior movimentação de veículos. O YOLO continuou realizando as detecções normalmente e o processamento funcionou sem apresentar travamentos significativos no computador.



Depois da validação da detecção, foi realizado um primeiro teste experimental de rastreamento e contagem de veículos utilizando a câmera ID 12, localizada no KM 193+000, sentido SÃO SEBASTIÃO. O sistema utilizou o tracking para acompanhar os objetos detectados e atribuir IDs individuais aos veículos. Uma linha virtual foi utilizada como referência para identificar quando um veículo passava pela região definida. Quando um veículo cruzava essa linha, seu ID era registrado e o contador era incrementado. Esse teste demonstrou que era possível utilizar YOLO juntamente com tracking para realizar uma primeira forma de contagem automática.



Posteriormente foi realizado outro teste utilizando a mesma câmera ID 12, mas sem exibir o vídeo na tela. A função de visualização foi removida para verificar como o sistema se comportaria executando somente o processamento em segundo plano. O teste iniciou corretamente, o stream foi aberto, o YOLO foi carregado e o sistema realizou a detecção e o tracking sem abrir uma janela de vídeo. Durante o teste foram registrados diferentes valores de processamento, incluindo aproximadamente 1,96 FPS, 7,64 FPS, 9,86 FPS, 4,85 FPS, 6,56 FPS e 6,71 FPS. Ao final do teste foram contabilizados experimentalmente 10 veículos. O teste demonstrou que o processamento pode ser realizado sem a necessidade de exibir continuamente o vídeo na tela, o que poderá ser interessante para uma futura execução contínua do sistema.



Apesar dos resultados positivos, a contagem realizada até o momento deve ser considerada apenas experimental. O sistema ainda não possui uma definição precisa da área da rodovia dentro da imagem. Também ainda não foram delimitados o acostamento, as faixas de circulação e os diferentes sentidos de tráfego. Além disso, o tracking ainda precisa ser estudado para verificar situações em que um veículo pode perder sua identificação ou receber um novo ID. Portanto, os números obtidos nos testes não devem ser considerados como uma contagem definitiva do tráfego.



Até o momento, a arquitetura básica validada experimentalmente pode ser representada da seguinte forma: API do DER → identificação da câmera → stream HLS (.m3u8) → OpenCV → captura de frames → YOLO → tracking → contagem experimental.



Os testes realizados permitiram validar várias etapas importantes do projeto. Foi confirmado o acesso à API do DER, a identificação das 11 câmeras da SP-055, a descoberta dos streams HLS, o funcionamento dos 11 streams testados, a captura de frames utilizando OpenCV, a detecção de veículos utilizando YOLO, o rastreamento experimental dos objetos e a realização de uma primeira contagem automática.



As próximas etapas de estudo deverão envolver a análise mais detalhada do comportamento do tracking, testes com diferentes volumes de tráfego, diferentes tipos de veículos, veículos parcialmente ocultos e diferentes condições de imagem. Posteriormente deverá ser desenvolvida uma forma de delimitar a área da rodovia dentro de cada câmera, separar o acostamento, identificar as faixas e definir os sentidos de circulação. Depois dessas etapas será possível trabalhar em uma contagem mais precisa, armazenamento dos dados, processamento contínuo e futuramente o processamento simultâneo das câmeras.



\## Estado atual



\- Acesso à API do DER: validado.

\- Identificação das câmeras: validado.

\- Streams HLS: validado.

\- 11 streams testados: 11 funcionando.

\- Captura de frames com OpenCV: validado nas 11 câmeras.

\- Detecção com YOLO: validada.

\- Tracking experimental: validado.

\- Contagem experimental: validada.

\- Processamento sem interface gráfica: validado.

\- Delimitação da área da rodovia: ainda não implementada.

\- Delimitação do acostamento: ainda não implementada.

\- Identificação das faixas: ainda não implementada.

\- Identificação dos sentidos: ainda não implementada.

\- Contagem definitiva: ainda não implementada.

\- Banco de dados e armazenamento dos resultados: ainda não implementados.

\- Monitoramento contínuo: ainda não implementado.

