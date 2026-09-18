
# ESCOPO DO PROJETO — ROADVISION

## 1. Identificação do Projeto

**Nome do projeto:** RoadVision
**Área:** Tecnologia da Informação / Inteligência Artificial / Análise de Tráfego
**Metodologia:** Scrum
**Equipe:** 4 integrantes
**Prazo estimado:** 13 semanas
**Repositório:** GitHub

---

## 2. Visão Geral do Projeto

O RoadVision é um sistema desenvolvido com o objetivo de utilizar imagens provenientes de câmeras rodoviárias para realizar a identificação e análise do fluxo de veículos por meio de técnicas de Inteligência Artificial e Visão Computacional.

O sistema utilizará câmeras disponibilizadas pelo Departamento de Estradas de Rodagem de São Paulo (DER/SP) como fonte de imagens. A partir dessas imagens, o RoadVision realizará o processamento dos frames e utilizará um modelo de detecção de objetos baseado em YOLO para identificar veículos presentes na rodovia.

A proposta é transformar as imagens das câmeras em dados estruturados que possam ser utilizados para compreender o fluxo de trânsito, incluindo a quantidade e os tipos de veículos identificados e, quando possível, o sentido em que esses veículos estão trafegando.

---

# 3. Problema

A análise do fluxo de veículos por meio de câmeras pode exigir acompanhamento manual das imagens, tornando o processo demorado e dificultando a obtenção de informações quantitativas de forma contínua.

Além disso, as imagens das câmeras possuem informações relevantes sobre o trânsito, mas essas informações precisam ser processadas para que possam ser transformadas em dados úteis para análise.

O RoadVision busca utilizar Inteligência Artificial para automatizar parte desse processo, permitindo que os veículos sejam identificados e contabilizados automaticamente a partir das imagens.

---

# 4. Objetivo Geral

Desenvolver um sistema capaz de utilizar imagens de câmeras rodoviárias para detectar, classificar e contabilizar veículos automaticamente, gerando dados que possibilitem a análise do fluxo de trânsito.

---

# 5. Objetivos Específicos

O projeto possui os seguintes objetivos:

* Integrar o sistema a câmeras rodoviárias disponíveis para acesso;
* Capturar imagens ou frames provenientes das câmeras;
* Processar as imagens utilizando técnicas de Visão Computacional;
* Implementar um modelo de Inteligência Artificial para detecção de veículos;
* Identificar diferentes categorias de veículos;
* Realizar a contagem dos veículos detectados;
* Desenvolver uma lógica para identificar o sentido do fluxo dos veículos;
* Armazenar os dados resultantes das análises;
* Organizar os dados para posterior consulta e visualização;
* Criar uma estrutura de software organizada e documentada;
* Validar o funcionamento do sistema por meio de testes.

---

# 6. Escopo do Produto

O produto desenvolvido será um sistema de monitoramento e análise automatizada do fluxo de veículos a partir de imagens de câmeras rodoviárias.

O sistema deverá ser capaz de:

### 6.1 Captura de imagens

O sistema deverá acessar uma câmera selecionada e obter imagens ou frames para processamento.

### 6.2 Detecção de veículos

Os frames capturados serão processados por um modelo de Inteligência Artificial baseado em YOLO, responsável pela identificação de objetos relacionados ao trânsito.

### 6.3 Classificação

Quando suportado pelo modelo utilizado, os veículos serão classificados em categorias, como:

* Carros;
* Motocicletas;
* Ônibus;
* Caminhões;
* Outros veículos reconhecidos pelo modelo.

### 6.4 Contagem de veículos

O sistema deverá contabilizar os veículos detectados, evitando, sempre que possível, que o mesmo veículo seja contado repetidamente.

### 6.5 Identificação de sentido

Será implementada uma lógica baseada na movimentação dos veículos na imagem para identificar o sentido do fluxo.

A análise poderá utilizar uma ou mais linhas virtuais de referência na imagem. Quando um veículo atravessar determinada região, o sistema registrará o evento e associará o veículo ao respectivo sentido.

### 6.6 Armazenamento

Os resultados obtidos pelo processamento poderão ser armazenados em banco de dados, permitindo a organização das informações coletadas.

Entre os dados que poderão ser registrados estão:

* Data e horário;
* Câmera utilizada;
* Local da câmera;
* Tipo de veículo;
* Quantidade de veículos;
* Sentido do fluxo;
* Informações relacionadas à detecção.

### 6.7 Visualização

Os dados coletados poderão ser apresentados por meio de uma interface ou ferramenta de visualização, permitindo acompanhar informações sobre o fluxo de veículos.

---

# 7. Funcionalidades do Sistema

As principais funcionalidades previstas são:

| Código | Funcionalidade                     |
| ------- | ---------------------------------- |
| RF01    | Selecionar uma câmera rodoviária |
| RF02    | Capturar imagens da câmera        |
| RF03    | Processar frames                   |
| RF04    | Detectar veículos                 |
| RF05    | Classificar veículos              |
| RF06    | Contabilizar veículos             |
| RF07    | Identificar o sentido do fluxo     |
| RF08    | Registrar os resultados            |
| RF09    | Armazenar os dados                 |
| RF10    | Consultar dados coletados          |
| RF11    | Apresentar informações de fluxo  |
| RF12    | Registrar erros de processamento   |

---

# 8. Requisitos Não Funcionais

O sistema também deverá atender a requisitos relacionados à qualidade e ao funcionamento.

### RNF01 — Desempenho

O sistema deverá processar os frames de maneira compatível com a capacidade do hardware disponível.

### RNF02 — Confiabilidade

O sistema deverá apresentar resultados consistentes durante os testes realizados.

### RNF03 — Manutenibilidade

O código deverá ser organizado de maneira que novos integrantes possam compreender e modificar o projeto.

### RNF04 — Portabilidade

O projeto deverá possuir instruções para configuração do ambiente de desenvolvimento em diferentes computadores.

### RNF05 — Documentação

As principais funcionalidades, configurações e procedimentos de execução deverão ser documentados.

### RNF06 — Versionamento

O código deverá ser versionado utilizando Git e GitHub, seguindo uma organização baseada em branches e Pull Requests.

---

# 9. Tecnologias Previstas

As tecnologias utilizadas no desenvolvimento poderão incluir:

* **Python** — linguagem principal;
* **YOLO / Ultralytics** — detecção de veículos;
* **OpenCV** — processamento de imagens;
* **Playwright** — automação e interação com a plataforma das câmeras;
* **PostgreSQL** — armazenamento dos dados;
* **Git** — controle de versão;
* **GitHub** — hospedagem e colaboração no código;
* **Visual Studio Code** — ambiente de desenvolvimento.

As tecnologias poderão ser ajustadas durante o desenvolvimento caso sejam identificadas alternativas mais adequadas.

---

# 10. Arquitetura Conceitual

O funcionamento geral do RoadVision seguirá o seguinte fluxo:

**Câmera DER/SP**

↓

**Captura de imagem/frame**

↓

**Processamento com OpenCV**

↓

**Modelo YOLO**

↓

**Detecção dos veículos**

↓

**Classificação**

↓

**Rastreamento/identificação da movimentação**

↓

**Contagem e identificação do sentido**

↓

**Armazenamento dos dados**

↓

**Visualização e análise**

---

# 11. Dados de Entrada

O principal dado de entrada do sistema será o conteúdo visual disponibilizado pelas câmeras rodoviárias.

Podem ser considerados como dados de entrada:

* Frames;
* Vídeos ou transmissões;
* Identificação da câmera;
* Localização da câmera;
* Data e horário da captura.

---

# 12. Dados de Saída

O sistema deverá produzir informações estruturadas a partir das imagens processadas.

Entre as principais saídas estão:

* Quantidade de veículos detectados;
* Categoria dos veículos;
* Sentido do fluxo;
* Data e horário da detecção;
* Identificação da câmera;
* Registros das análises realizadas.

Esses dados poderão posteriormente ser utilizados para geração de gráficos, relatórios ou outros recursos de análise.

---

# 13. Fora do Escopo

Para evitar o crescimento descontrolado do projeto, algumas funcionalidades não fazem parte da versão inicial do RoadVision.

Estão fora do escopo:

* Reconhecimento de placas de veículos;
* Identificação pessoal dos motoristas ou passageiros;
* Aplicação automática de multas;
* Controle de semáforos;
* Controle físico de rodovias;
* Comunicação direta com equipamentos de fiscalização;
* Previsão avançada de congestionamentos;
* Desenvolvimento de câmeras ou equipamentos físicos;
* Desenvolvimento de aplicativo mobile na primeira versão;
* Reconhecimento facial;
* Identificação individual de pessoas.

Essas funcionalidades poderão ser consideradas futuramente, caso o projeto evolua para novas versões.

---

# 14. Restrições do Projeto

O desenvolvimento do RoadVision possui algumas limitações que deverão ser consideradas:

* Dependência da disponibilidade das câmeras utilizadas;
* Qualidade e resolução das imagens disponibilizadas;
* Possíveis interrupções ou alterações no acesso às câmeras;
* Capacidade de processamento dos computadores utilizados pela equipe;
* Limitações do modelo de Inteligência Artificial;
* Prazo de desenvolvimento de 13 semanas;
* Disponibilidade dos integrantes da equipe;
* Necessidade de aprendizado de novas tecnologias pela equipe.

---

# 15. Premissas

Para o desenvolvimento do projeto, serão consideradas as seguintes premissas:

* As câmeras utilizadas estarão acessíveis durante os períodos necessários para os testes;
* As imagens possuirão qualidade suficiente para permitir a detecção dos veículos;
* O modelo YOLO será capaz de identificar parte significativa das categorias de veículos desejadas;
* A equipe terá acesso aos ambientes necessários para desenvolvimento;
* O GitHub será utilizado como principal ferramenta de versionamento e colaboração;
* O desenvolvimento seguirá a metodologia Scrum;
* O projeto será desenvolvido de forma incremental, permitindo validar cada funcionalidade antes de avançar para a próxima etapa.

---

# 16. Entregas do Projeto

Ao longo do desenvolvimento, estão previstas as seguintes entregas:

### Entrega 1 — Ambiente de desenvolvimento

* Repositório configurado;
* Estrutura de pastas;
* Ambiente Python;
* Dependências documentadas;
* Configuração do Git/GitHub.

### Entrega 2 — Integração com câmera

* Acesso à câmera;
* Seleção da câmera;
* Captura dos frames.

### Entrega 3 — Inteligência Artificial

* Modelo YOLO configurado;
* Detecção de veículos;
* Classificação dos veículos.

### Entrega 4 — Contagem e sentido

* Contagem dos veículos;
* Rastreamento da movimentação;
* Identificação dos sentidos.

### Entrega 5 — Armazenamento

* Estrutura do banco de dados;
* Registro das informações;
* Integração do sistema com o banco.

### Entrega 6 — Visualização

* Apresentação dos dados;
* Gráficos ou indicadores;
* Informações sobre fluxo de veículos.

### Entrega 7 — Documentação e validação

* Documentação técnica;
* Testes;
* Correção de problemas;
* Organização final do repositório;
* Apresentação do projeto.

---

# 17. Critérios de Aceitação

O RoadVision será considerado funcional quando conseguir, dentro das condições de teste:

1. Acessar uma câmera configurada;
2. Capturar imagens ou frames;
3. Processar os frames corretamente;
4. Detectar veículos nas imagens;
5. Identificar categorias de veículos suportadas;
6. Realizar a contagem dos veículos;
7. Identificar o sentido do fluxo em condições adequadas;
8. Registrar os resultados;
9. Armazenar os dados corretamente;
10. Apresentar os resultados de maneira compreensível;
11. Executar o sistema seguindo a documentação fornecida.

Os resultados deverão ser avaliados considerando as limitações de qualidade das imagens, posicionamento da câmera, iluminação, oclusões e capacidade do modelo utilizado.

---

# 18. Metodologia de Desenvolvimento

O desenvolvimento será realizado utilizando a metodologia ágil Scrum.

O projeto será dividido em Sprints, permitindo que as funcionalidades sejam desenvolvidas de forma incremental.

Cada Sprint deverá possuir:

* Planejamento;
* Definição das tarefas;
* Desenvolvimento;
* Testes;
* Revisão;
* Registro dos resultados;
* Identificação de problemas;
* Planejamento das próximas atividades.

O GitHub será utilizado para controle de versão, enquanto o Jira será utilizado para organização e acompanhamento das atividades.

---

# 19. Estrutura de Gestão do Projeto

A equipe será composta por quatro integrantes.

As responsabilidades poderão ser distribuídas de acordo com as necessidades do projeto, envolvendo:

* Desenvolvimento do sistema;
* Inteligência Artificial e Visão Computacional;
* Banco de dados;
* Integração com as câmeras;
* Testes;
* Documentação;
* Gerenciamento do projeto.

As responsabilidades poderão ser compartilhadas entre os integrantes conforme a evolução das Sprints.

---

# 20. Cronograma Macro

O projeto terá duração estimada de 13 semanas.

### Semanas 1–3 — Preparação

* Definição dos requisitos;
* Organização do projeto;
* Configuração do ambiente;
* Estruturação do GitHub;
* Primeiros testes de acesso às câmeras.

### Semanas 4–6 — Integração

* Desenvolvimento da captura;
* Integração com as câmeras;
* Processamento dos frames;
* Primeiros testes com imagens reais.

### Semanas 7–9 — Inteligência Artificial

* Implementação do YOLO;
* Detecção de veículos;
* Classificação;
* Testes e ajustes.

### Semanas 10–11 — Contagem e análise

* Rastreamento;
* Contagem;
* Identificação de sentido;
* Armazenamento dos dados.

### Semanas 12–13 — Finalização

* Visualização dos resultados;
* Testes finais;
* Correções;
* Documentação;
* Organização do repositório;
* Apresentação final.

---

# 21. Riscos Principais

| Risco                             | Impacto     | Estratégia                                          |
| --------------------------------- | ----------- | ---------------------------------------------------- |
| Câmera indisponível             | Alto        | Utilizar outra câmera ou vídeos de teste           |
| Baixa qualidade da imagem         | Alto        | Testar diferentes câmeras e ajustar o processamento |
| Baixo desempenho do computador    | Médio/Alto | Otimizar resolução e processamento                 |
| Modelo não detectar corretamente | Alto        | Ajustar parâmetros e realizar novos testes          |
| Alteração no site das câmeras  | Alto        | Adaptar a integração                               |
| Problemas de integração         | Médio      | Realizar testes incrementais                         |
| Falta de conhecimento técnico    | Médio      | Documentação e estudo das tecnologias              |
| Atraso nas Sprints                | Médio      | Priorizar funcionalidades essenciais                 |

---

# 22. Limitações Conhecidas

Os resultados do sistema não deverão ser considerados perfeitos.

A precisão da detecção poderá ser afetada por:

* Chuva;
* Neblina;
* Baixa iluminação;
* Imagens com baixa resolução;
* Veículos parcialmente ocultos;
* Grande quantidade de veículos simultaneamente;
* Distância entre a câmera e os veículos;
* Ângulo da câmera;
* Obstruções;
* Variações na transmissão das imagens.

Portanto, os resultados deverão ser interpretados como **dados estimados pelo sistema de Visão Computacional**, e não como uma contagem oficial de tráfego.

---

# 23. Indicadores de Sucesso

O sucesso do projeto será avaliado principalmente pela capacidade de:

* Capturar imagens de uma câmera real;
* Detectar veículos automaticamente;
* Classificar os veículos;
* Contabilizar veículos;
* Identificar o sentido do fluxo;
* Registrar os dados;
* Apresentar os resultados;
* Manter o código organizado e documentado;
* Permitir que outro integrante consiga configurar e executar o projeto.

---

# 24. Definição de Pronto — Definition of Done

Uma funcionalidade será considerada concluída quando:

* O código estiver implementado;
* O código estiver organizado;
* A funcionalidade tiver sido testada;
* Os erros críticos tiverem sido corrigidos;
* A implementação estiver integrada ao projeto;
* O código estiver versionado no GitHub;
* A documentação necessária estiver atualizada;
* A equipe tiver validado a funcionalidade.

---

# 25. Resultado Esperado

Ao final das 13 semanas, espera-se que o RoadVision possua uma versão funcional capaz de acessar uma câmera rodoviária, processar suas imagens utilizando técnicas de Visão Computacional e Inteligência Artificial, detectar e classificar veículos, realizar sua contagem e identificar o sentido do fluxo em condições adequadas.

Os dados gerados deverão ser organizados e armazenados de maneira que possam ser utilizados para análise e visualização.

O projeto também deverá possuir código-fonte organizado, documentação técnica, histórico de desenvolvimento no GitHub e evidências dos testes realizados.

---

# 26. Considerações Finais

O RoadVision será desenvolvido de forma incremental, priorizando inicialmente a construção de uma versão mínima funcional do sistema.

A prioridade será garantir que o fluxo principal — **captura → detecção → classificação → contagem → identificação de sentido → armazenamento** — funcione corretamente antes da implementação de funcionalidades adicionais.

Alterações no escopo deverão ser avaliadas pela equipe antes de serem incorporadas ao projeto, considerando seu impacto no prazo, nas funcionalidades existentes e nos objetivos definidos.

Dessa forma, o escopo servirá como referência para o planejamento das Sprints, organização das tarefas no Trello, desenvolvimento no GitHub e avaliação final do projeto.
