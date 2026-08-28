
# 🚀 Como Começar no RoadVision

Este documento apresenta o passo a passo para um novo integrante começar a trabalhar no projeto RoadVision.

O objetivo é explicar o caminho desde o primeiro acesso ao projeto até o início de uma tarefa.

---

# 1. 👋 Entendendo o RoadVision

O RoadVision é um sistema de monitoramento inteligente de rodovias que utiliza Visão Computacional e Inteligência Artificial para analisar imagens provenientes de câmeras rodoviárias.

O objetivo do projeto é transformar imagens das rodovias em informações úteis para análise do tráfego.

Entre as funcionalidades planejadas estão:

- identificação de veículos;
- classificação de veículos;
- contagem de veículos;
- identificação do sentido do tráfego;
- análise do fluxo;
- identificação de situações anormais;
- geração de informações para monitoramento.

Antes de começar a desenvolver, recomenda-se entender o objetivo geral do projeto e consultar o README principal.

---

# 2. 📚 Conhecendo o projeto

O primeiro arquivo que deve ser consultado é:

    README.md

O README apresenta:

- objetivo do projeto;
- tecnologias utilizadas;
- estrutura das pastas;
- status do desenvolvimento;
- fluxo geral do projeto;
- documentação disponível.

Depois de conhecer o projeto, consulte os documentos disponíveis na pasta `docs`.

---

# 3. 📖 Documentação

A documentação principal está organizada da seguinte forma:

## Configuração do Ambiente

Arquivo:

    docs/CONFIGURACAO_AMBIENTE.md

Utilize esse documento para configurar:

- Python;
- Git;
- Visual Studio Code;
- ambiente virtual;
- dependências;
- Playwright;
- testes iniciais.

---

## Guia do Desenvolvedor

Arquivo:

    docs/GUIA_DESENVOLVEDOR.md

Utilize esse documento para aprender:

- como utilizar o Git;
- como criar branches;
- como realizar commits;
- como enviar código para o GitHub;
- como criar Pull Requests;
- como participar de Code Reviews;
- como realizar o fluxo de Merge;
- como relacionar o trabalho ao Trello.

---

# 4. 💻 Preparando o computador

Antes de começar a desenvolver, configure seu ambiente seguindo:

    docs/CONFIGURACAO_AMBIENTE.md

Não pule essa etapa.

Todos os integrantes devem possuir um ambiente de desenvolvimento configurado de maneira semelhante.

---

# 5. 📥 Obtendo o projeto

Depois de possuir Git instalado, clone o repositório oficial:

    git clone URL_DO_REPOSITORIO

Entre na pasta:

    cd RoadVision

Abra o projeto no Visual Studio Code:

    code .

---

# 6. 🐍 Configurando o ambiente Python

Dentro da pasta do projeto, crie o ambiente virtual:

    py -3.12 -m venv .venv

Ative o ambiente:

    .venv\Scripts\Activate.ps1

Depois instale as dependências:

    pip install -r requirements.txt

Instale os navegadores necessários para o Playwright:

    playwright install

Para obter todos os detalhes, consulte:

    docs/CONFIGURACAO_AMBIENTE.md

---

# 7. 🧪 Verificando se tudo está funcionando

Depois de configurar o ambiente, execute o teste:

    python tests/test_ambiente.py

Se o teste funcionar sem erros, o ambiente básico está pronto.

Caso apareça algum erro, consulte a seção de problemas comuns do documento de configuração.

---

# 8. 📋 Conhecendo o Trello

O Trello é utilizado pela equipe para organizar as tarefas do projeto.

Antes de começar uma atividade, consulte o quadro do projeto.

As tarefas podem conter:

- título;
- descrição;
- responsável;
- prioridade;
- checklist;
- prazo;
- observações;
- links relacionados.

Escolha uma tarefa atribuída a você e leia todas as informações antes de começar.

---

# 9. 🌿 Criando uma branch

Cada tarefa deve ser desenvolvida em uma branch própria.

Primeiro atualize a `main`:

    git switch main

Depois:

    git pull

Crie uma branch para a tarefa:

    git switch -c nome-da-branch

Exemplo:

    git switch -c feature/deteccao-veiculos

O nome da branch deve representar a tarefa que está sendo desenvolvida.

---

# 10. 💻 Desenvolvendo

Com a branch criada, comece o desenvolvimento.

Durante essa etapa:

- trabalhe somente na tarefa selecionada;
- mantenha o código organizado;
- siga a estrutura existente;
- evite alterações desnecessárias;
- teste o que foi desenvolvido;
- documente alterações importantes.

Se surgir uma dúvida sobre o projeto, consulte primeiro a documentação.

---

# 11. 🧪 Testando

Antes de enviar o código para revisão, execute os testes necessários.

Verifique:

- se o código funciona;
- se não existem erros;
- se a funcionalidade foi realmente implementada;
- se funcionalidades existentes continuam funcionando.

Quando aplicável:

    python -m pytest

Também pode ser utilizado um teste específico:

    python tests/test_ambiente.py

---

# 12. 💾 Criando o commit

Depois de concluir e testar a tarefa:

    git status

Verifique as alterações.

Depois:

    git add .

Crie o commit:

    git commit -m "mensagem"

Exemplo:

    git commit -m "feat: adiciona deteccao de veiculos"

A mensagem deve explicar claramente o que foi alterado.

---

# 13. 📤 Enviando para o GitHub

Envie sua branch:

    git push -u origin nome-da-branch

Exemplo:

    git push -u origin feature/deteccao-veiculos

Depois disso, sua branch estará disponível no GitHub.

---

# 14. 🔀 Criando um Pull Request

No GitHub, crie um Pull Request direcionado para a `main`.

O Pull Request deve explicar:

- o que foi desenvolvido;
- qual tarefa foi realizada;
- como foi testado;
- possíveis observações.

Sempre que possível, coloque o link ou número do Pull Request no card correspondente do Trello.

---

# 15. 👀 Revisão

Outro integrante da equipe deverá revisar o Pull Request.

A revisão poderá resultar em:

    ✅ Aprovação

ou:

    🔄 Solicitação de alterações

Caso sejam solicitadas alterações, faça as correções na mesma branch e envie novamente:

    git add .
    git commit -m "fix: realiza ajustes solicitados"
    git push

O Pull Request será atualizado automaticamente.

---

# 16. 🔀 Merge

Depois da aprovação, o Pull Request poderá ser integrado à `main`.

O Merge incorpora as alterações da sua branch à versão principal do projeto.

Após o Merge, a tarefa poderá ser considerada concluída.

---

# 17. 📋 Finalizando a tarefa no Trello

Depois do Merge:

1. Confirme que o Pull Request foi integrado;
2. Atualize o card do Trello;
3. Adicione observações importantes;
4. Mova o card para `Concluído`.

O ciclo completo é:

    Trello
      ↓
    Branch
      ↓
    Desenvolvimento
      ↓
    Testes
      ↓
    Commit
      ↓
    Push
      ↓
    Pull Request
      ↓
    Review
      ↓
    Merge
      ↓
    Trello → Concluído

---

# 18. 🔄 Começando uma nova tarefa

Depois de finalizar uma tarefa, não continue trabalhando na branch anterior.

Volte para a `main`:

    git switch main

Atualize:

    git pull

Crie uma nova branch:

    git switch -c nome-da-nova-branch

Cada tarefa deve possuir sua própria branch.

---

# 19. 🧠 Regras importantes

## Nunca desenvolva diretamente na `main`

A `main` representa a versão principal do projeto.

---

## Nunca envie a `.venv`

O ambiente virtual pertence ao computador de cada desenvolvedor.

---

## Nunca envie informações sensíveis

Não envie:

- senhas;
- tokens;
- chaves de API;
- arquivos `.env`;
- credenciais.

---

## Não faça alterações fora da tarefa

Evite modificar arquivos que não tenham relação com a atividade.

Se uma alteração adicional for necessária, informe a equipe.

---

# 20. 🆘 Se precisar de ajuda

Caso não consiga realizar alguma etapa, não apague arquivos ou o repositório para tentar corrigir o problema.

Primeiro execute:

    git status

Depois:

    git branch

E envie para a equipe:

1. o que você estava tentando fazer;
2. o comando executado;
3. a mensagem completa do erro;
4. a branch atual;
5. o resultado do `git status`.

Uma captura de tela também pode ser enviada.

---

# 21. 🤖 Como pedir ajuda para uma IA

Caso utilize uma Inteligência Artificial para ajudar a solucionar um problema, forneça o máximo de contexto possível.

Um bom pedido deve informar:

- objetivo da tarefa;
- estrutura relevante do projeto;
- código relacionado ao problema;
- mensagem completa do erro;
- sistema operacional;
- versão do Python;
- comando que foi executado;
- o que já foi tentado.

### Exemplo

    Estou trabalhando no projeto RoadVision.

    Estou desenvolvendo a tarefa "detecção de veículos".

    Estou utilizando Python 3.12, OpenCV e Ultralytics.

    Ao executar o arquivo X acontece o seguinte erro:

    [cole o erro completo]

    Já tentei:

    [descreva o que foi tentado]

    Analise o problema e explique a causa antes de sugerir a correção.

A IA deve ser utilizada como ferramenta de apoio. O desenvolvedor continua responsável por compreender e testar as alterações realizadas.

---

# 22. ✅ Checklist para começar

Antes de iniciar sua primeira tarefa, confirme:

- [ ] Li o README.md
- [ ] Entendi o objetivo do RoadVision
- [ ] Configurei o ambiente
- [ ] Clonei o repositório
- [ ] Abri o projeto no VS Code
- [ ] Ativei o `.venv`
- [ ] Instalei as dependências
- [ ] Executei os testes
- [ ] Acessei o Trello
- [ ] Identifiquei minha tarefa
- [ ] Entendi os critérios da tarefa
- [ ] Criei minha branch
- [ ] Estou pronto para desenvolver

---

# 🚗 Bem-vindo ao RoadVision!

Depois de concluir este documento, você estará preparado para começar a desenvolver no projeto.

Em caso de dúvida, consulte primeiro a documentação existente antes de realizar alterações estruturais no projeto.

**RoadVision — Transformando imagens de rodovias em informações inteligentes.**
