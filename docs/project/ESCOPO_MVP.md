 

# ESCOPO DO MVP — ROADVISION

## 1. Identificação

**Projeto:** RoadVision
**Documento:** Escopo do MVP
**Metodologia:** Scrum
**Área:** Inteligência Artificial e Visão Computacional
**Versão:** 1.0

---

## 2. Introdução

O RoadVision é um projeto que tem como objetivo utilizar técnicas de Inteligência Artificial e Visão Computacional para realizar a análise automatizada do fluxo de veículos em rodovias.

O projeto utilizará imagens provenientes de câmeras rodoviárias como fonte de dados. Essas imagens serão processadas por ferramentas de Visão Computacional e por um modelo de detecção baseado em YOLO, permitindo identificar veículos presentes nos frames.

Para validar a proposta de forma incremental, será desenvolvido inicialmente um **Produto Mínimo Viável (MVP)**. O MVP terá como foco implementar somente as funcionalidades essenciais para comprovar a viabilidade técnica do RoadVision.

---

# 3. Objetivo do MVP

O objetivo do MVP é desenvolver uma primeira versão funcional do RoadVision capaz de:

* acessar uma câmera rodoviária;
* capturar imagens ou frames;
* processar os frames;
* detectar veículos utilizando Inteligência Artificial;
* classificar os veículos identificados;
* realizar a contagem dos veículos;
* apresentar os resultados de forma visual.

O MVP será utilizado como base para validar a proposta do projeto antes da implementação de funcionalidades mais avançadas.

---

# 4. Problema que o MVP Busca Resolver

A análise manual de imagens de câmeras rodoviárias pode exigir acompanhamento constante e dificultar a obtenção de dados quantitativos sobre o fluxo de veículos.

O MVP busca demonstrar que é possível utilizar Inteligência Artificial para transformar imagens de câmeras rodoviárias em informações estruturadas sobre os veículos presentes na cena.

---

# 5. Escopo Funcional do MVP

O MVP será composto pelas seguintes funcionalidades.

## 5.1 Acesso à câmera

O sistema deverá ser capaz de acessar uma câmera rodoviária selecionada para obter imagens destinadas ao processamento.

Inicialmente, será utilizada **uma câmera**, permitindo que a equipe valide o funcionamento do sistema antes de expandir para múltiplas câmeras.

---

## 5.2 Captura dos frames

Após o acesso à câmera, o sistema deverá obter frames da transmissão para serem utilizados como entrada no processo de análise.

A captura deverá ser realizada de maneira que os frames possam ser enviados para o módulo de processamento de imagens.

---

## 5.3 Processamento das imagens

Os frames capturados deverão passar por um processo de preparação utilizando ferramentas de Visão Computacional.

O processamento poderá incluir:

* ajuste de resolução;
* conversão de formato;
* preparação do frame para o modelo de Inteligência Artificial;
* outras operações necessárias para melhorar o processamento.

---

## 5.4 Detecção de veículos

O sistema utilizará um modelo YOLO para identificar objetos presentes nos frames.

O foco do MVP será a detecção de veículos relacionados ao trânsito rodoviário.

Quando um veículo for identificado, o sistema deverá apresentar visualmente a detecção, por exemplo, utilizando caixas delimitadoras sobre o objeto.

---

## 5.5 Classificação dos veículos

Quando suportado pelo modelo utilizado, os veículos detectados deverão ser classificados de acordo com as categorias reconhecidas.

Entre as categorias previstas estão:

* Carros;
* Motocicletas;
* Ônibus;
* Caminhões.

A quantidade de categorias poderá variar de acordo com o modelo utilizado e com os resultados obtidos durante os testes.

---

## 5.6 Contagem de veículos

O sistema deverá realizar a contagem dos veículos identificados durante o processamento.

O objetivo inicial será obter uma contagem funcional dos veículos detectados.

Em versões posteriores, poderão ser implementadas técnicas mais avançadas de rastreamento para reduzir a possibilidade de um mesmo veículo ser contabilizado várias vezes.

---

## 5.7 Visualização dos resultados

O MVP deverá apresentar os resultados do processamento de forma visual.

A interface inicial poderá apresentar:

* imagem ou frame processado;
* caixas de detecção;
* categoria do veículo;
* quantidade de veículos identificados.

A visualização será inicialmente simples, priorizando a validação da funcionalidade em vez de uma interface final.

---

# 6. Fluxo do MVP

O funcionamento do MVP seguirá, inicialmente, o seguinte fluxo:

```text
Câmera rodoviária
        ↓
Captura do frame
        ↓
Processamento da imagem
        ↓
Modelo YOLO
        ↓
Detecção dos veículos
        ↓
Classificação
        ↓
Contagem
        ↓
Visualização dos resultados
```

---

# 7. Tecnologias do MVP

As principais tecnologias previstas para o desenvolvimento são:

| Tecnologia         | Função                                      |
| ------------------ | --------------------------------------------- |
| Python             | Desenvolvimento da aplicação                |
| YOLO / Ultralytics | Detecção de objetos                         |
| OpenCV             | Processamento de imagens                      |
| Playwright         | Acesso e automação da plataforma da câmera |
| Git                | Controle de versão                           |
| GitHub             | Hospedagem e colaboração                    |
| Visual Studio Code | Ambiente de desenvolvimento                   |

As tecnologias poderão ser modificadas caso a equipe identifique soluções mais adequadas durante o desenvolvimento.

---

# 8. Dados de Entrada

O principal dado de entrada do MVP será a imagem proveniente da câmera rodoviária.

Os dados poderão incluir:

* Frames da câmera;
* Identificação da câmera;
* Data e horário da captura;
* Informações básicas relacionadas à câmera.

---

# 9. Dados de Saída

O MVP deverá produzir informações relacionadas aos veículos detectados.

Entre as principais saídas estão:

* Veículos identificados;
* Categoria do veículo;
* Quantidade de veículos detectados;
* Imagem processada;
* Informações referentes ao processamento.

---

# 10. Fora do Escopo do MVP

Para manter o desenvolvimento dentro de um tamanho adequado, as seguintes funcionalidades não fazem parte da primeira versão:

* Identificação de placas;
* Reconhecimento facial;
* Identificação de motoristas;
* Aplicação de multas;
* Controle de semáforos;
* Controle físico de rodovias;
* Previsão de congestionamentos;
* Dashboard completo;
* Aplicativo mobile;
* Processamento simultâneo de diversas câmeras;
* Sistema avançado de relatórios;
* Integração com sistemas externos de fiscalização;
* Análise preditiva avançada.

Essas funcionalidades poderão ser consideradas em versões futuras do RoadVision.

---

# 11. Requisitos Funcionais do MVP

| Código  | Requisito                                                                 |
| -------- | ------------------------------------------------------------------------- |
| MVP-RF01 | O sistema deverá acessar uma câmera configurada.                        |
| MVP-RF02 | O sistema deverá capturar frames da câmera.                             |
| MVP-RF03 | O sistema deverá processar os frames capturados.                         |
| MVP-RF04 | O sistema deverá detectar veículos utilizando YOLO.                     |
| MVP-RF05 | O sistema deverá classificar os veículos quando suportado pelo modelo.  |
| MVP-RF06 | O sistema deverá realizar a contagem dos veículos detectados.           |
| MVP-RF07 | O sistema deverá apresentar visualmente os veículos detectados.         |
| MVP-RF08 | O sistema deverá apresentar informações básicas sobre as detecções. |

---

# 12. Requisitos Não Funcionais do MVP

### MVP-RNF01 — Desempenho

O sistema deverá apresentar desempenho compatível com o hardware disponível para a equipe.

### MVP-RNF02 — Organização

O código deverá ser organizado em módulos e arquivos de acordo com a estrutura definida para o projeto.

### MVP-RNF03 — Manutenibilidade

A estrutura deverá permitir futuras alterações e inclusão de novas funcionalidades.

### MVP-RNF04 — Versionamento

O código deverá ser mantido em um repositório GitHub utilizando branches para desenvolvimento das funcionalidades.

### MVP-RNF05 — Documentação

As principais etapas de instalação, configuração e execução deverão estar documentadas.

---

# 13. Critérios de Aceitação

O MVP será considerado funcional quando:

1. O sistema conseguir acessar uma câmera configurada;
2. Conseguir obter frames da câmera;
3. Conseguir processar os frames;
4. O modelo YOLO conseguir detectar veículos;
5. Os veículos detectados forem apresentados visualmente;
6. As categorias reconhecidas pelo modelo forem apresentadas;
7. O sistema conseguir realizar uma contagem dos veículos detectados;
8. O processo puder ser executado seguindo as instruções de configuração;
9. Os principais erros encontrados durante os testes forem registrados e tratados.

---

# 14. Limitações do MVP

Os resultados do MVP estarão sujeitos às condições das imagens utilizadas.

A eficiência da detecção poderá ser afetada por:

* baixa resolução;
* iluminação;
* chuva;
* neblina;
* distância dos veículos;
* ângulo da câmera;
* veículos parcialmente ocultos;
* quantidade de veículos na imagem;
* desempenho do computador;
* limitações do modelo de Inteligência Artificial.

Por esse motivo, o MVP será considerado uma **prova de conceito funcional**, e não um sistema de monitoramento rodoviário pronto para utilização operacional.

---

# 15. Riscos do MVP

| Risco                                       | Impacto     | Mitigação                                            |
| ------------------------------------------- | ----------- | ------------------------------------------------------ |
| Câmera indisponível                       | Alto        | Utilizar outra câmera ou imagens gravadas para testes |
| Baixa qualidade da imagem                   | Alto        | Testar outras câmeras e ajustar o processamento       |
| Modelo não detectar veículos corretamente | Alto        | Ajustar parâmetros e testar diferentes modelos        |
| Baixo desempenho do computador              | Médio/Alto | Reduzir resolução e quantidade de frames processados |
| Alteração na plataforma da câmera        | Alto        | Adaptar o módulo de integração                      |
| Problemas de instalação                   | Médio      | Manter documentação de configuração do ambiente    |

---

# 16. Evolução Após o MVP

Após a validação do MVP, novas funcionalidades poderão ser incorporadas ao RoadVision de maneira incremental.

Entre as possíveis evoluções estão:

### Versão 2

* Rastreamento dos veículos;
* Melhoria da contagem;
* Identificação do sentido do fluxo;
* Armazenamento dos dados.

### Versão 3

* Integração com banco de dados;
* Processamento de múltiplas câmeras;
* Histórico das informações;
* Dashboard de visualização.

### Versões futuras

* Análise de fluxo por períodos;
* Indicadores de trânsito;
* Análises estatísticas;
* Recursos preditivos;
* Outras funcionalidades definidas pela equipe.

---

# 17. Definition of Done do MVP

O MVP será considerado concluído quando:

* O código estiver implementado;
* A integração com uma câmera estiver funcionando;
* A captura de frames estiver funcionando;
* O modelo YOLO estiver configurado;
* A detecção de veículos estiver funcionando;
* A classificação estiver funcionando dentro das capacidades do modelo;
* A contagem estiver implementada;
* Os resultados estiverem sendo apresentados;
* Os testes principais tiverem sido realizados;
* Os erros críticos tiverem sido corrigidos;
* O código estiver versionado no GitHub;
* A documentação básica estiver atualizada.

---

# 18. Resultado Esperado

Ao final do desenvolvimento do MVP, espera-se possuir uma primeira versão funcional do RoadVision capaz de utilizar uma câmera rodoviária como fonte de imagens e aplicar Inteligência Artificial para detectar, classificar e contabilizar veículos.

O MVP deverá demonstrar a **viabilidade técnica da proposta principal do RoadVision**, servindo como base para o desenvolvimento das funcionalidades futuras.

---

# 19. Conclusão

O MVP do RoadVision foi definido com foco nas funcionalidades essenciais para validar a proposta do projeto.

A estratégia será começar com uma única câmera e um fluxo simplificado de processamento, evitando que funcionalidades secundárias aumentem desnecessariamente a complexidade da primeira versão.

Dessa forma, a equipe poderá validar inicialmente o funcionamento da integração com a câmera e da detecção de veículos antes de avançar para recursos mais complexos, como rastreamento, identificação de sentido, armazenamento, dashboards e análises avançadas.

O escopo do MVP também servirá como referência para a definição das tarefas, organização das Sprints e acompanhamento do desenvolvimento do RoadVision.
