# ⚙️ Configuração do Ambiente de Desenvolvimento — RoadVision

Este documento apresenta o passo a passo necessário para configurar o ambiente de desenvolvimento do projeto RoadVision.

O objetivo é permitir que qualquer integrante da equipe consiga preparar sua máquina, acessar o projeto, instalar as dependências e executar os testes necessários sem depender da configuração feita por outro integrante.

---

## 1. 📋 Sobre o ambiente

O RoadVision é desenvolvido utilizando Python e possui recursos relacionados a visão computacional, Inteligência Artificial e automação.

As principais tecnologias utilizadas atualmente são:

- Python 3.12
- Git
- GitHub
- Visual Studio Code
- OpenCV
- Ultralytics / YOLO
- Playwright
- NumPy
- PyTorch
- outras bibliotecas presentes no `requirements.txt`

Cada integrante deve possuir seu próprio ambiente virtual Python para evitar conflitos entre versões e dependências instaladas no computador.

---

## 2. 💻 Programas necessários

Antes de iniciar a configuração do projeto, é necessário possuir os seguintes programas instalados:

### Python

O projeto utiliza Python 3.12.

Para verificar se o Python está instalado, abra o PowerShell ou o terminal do VS Code e execute:

    py --version

Também é possível verificar especificamente a versão 3.12:

    py -3.12 --version

O resultado esperado será semelhante a:

    Python 3.12.x

Caso o comando `py -3.12` não funcione, a instalação do Python 3.12 deverá ser realizada antes de continuar.

---

### Git

O Git é utilizado para controlar as versões do projeto e permitir que os integrantes trabalhem de forma colaborativa através do GitHub.

Para verificar a instalação:

    git --version

Se o comando retornar uma versão do Git, a instalação está funcionando.

---

### Visual Studio Code

O Visual Studio Code será utilizado como principal editor de código do projeto.

Depois de instalar o VS Code, recomenda-se instalar as extensões necessárias para Python e Git.

---

## 3. 📥 Acessando o projeto

O código-fonte do RoadVision está armazenado no GitHub.

O integrante deverá acessar o repositório oficial fornecido pela equipe.

Na página do GitHub, clique em:

    Code → HTTPS

Copie o endereço do repositório.

No terminal, escolha o local onde deseja armazenar o projeto e execute:

    git clone URL_DO_REPOSITORIO

Substitua `URL_DO_REPOSITORIO` pelo endereço real do repositório.

Depois entre na pasta:

    cd RoadVision

A partir desse momento, todos os comandos deverão ser executados dentro da pasta principal do projeto.

---

## 4. 📂 Abrindo o projeto no VS Code

Com o terminal dentro da pasta `RoadVision`, execute:

    code .

O projeto será aberto no Visual Studio Code.

Também é possível abrir o VS Code manualmente e selecionar:

    File → Open Folder

Depois selecione a pasta principal do RoadVision.

É importante abrir a pasta principal do projeto e não uma subpasta como `src`, `tests` ou `models`.

---

## 5. 🐍 Criando o ambiente virtual

Cada integrante deve possuir seu próprio ambiente virtual.

O ambiente virtual permite que as dependências do RoadVision sejam instaladas de forma isolada, sem interferir em outros projetos Python instalados no computador.

Dentro da pasta principal do projeto, execute:

    py -3.12 -m venv .venv

Após a execução, será criada uma pasta chamada:

    .venv

Essa pasta é utilizada somente no computador de cada desenvolvedor e não deve ser enviada para o GitHub.

---

## 6. ▶️ Ativando o ambiente virtual

No Windows PowerShell, execute:

    .venv\Scripts\Activate.ps1

Quando o ambiente estiver ativo, o terminal deverá apresentar algo semelhante a:

    (.venv) PS C:\...\RoadVision>

O indicador `(.venv)` significa que o ambiente virtual está ativo.

Sempre que for desenvolver ou executar o projeto, verifique se o ambiente virtual está ativado.

---

## 7. 📦 Instalando as dependências

Com o ambiente virtual ativado, execute:

    python -m pip install --upgrade pip

Depois instale as dependências do projeto:

    pip install -r requirements.txt

O arquivo `requirements.txt` contém as bibliotecas necessárias para o funcionamento do RoadVision.

Não é recomendado instalar bibliotecas aleatoriamente sem atualizar a documentação e o arquivo de dependências do projeto.

---

## 8. 🎭 Configurando o Playwright

O projeto utiliza Playwright para automação relacionada ao acesso às câmeras.

Depois de instalar as bibliotecas, execute:

    playwright install

Esse comando instala os navegadores necessários para o funcionamento do Playwright.

---

## 9. 🧪 Testando a configuração

Depois de concluir a instalação, o ambiente deve ser testado.

Execute:

    python tests/test_ambiente.py

Caso o teste seja executado sem erros, significa que a configuração básica do ambiente está funcionando.

Caso ocorra algum erro, verifique:

- versão do Python;
- ambiente virtual ativado;
- dependências instaladas;
- instalação do Playwright;
- localização correta da pasta do projeto.

---

## 10. 📁 Estrutura do projeto

A estrutura principal do RoadVision é organizada da seguinte maneira:

    RoadVision/
    │
    ├── data/
    │
    ├── docs/
    │
    ├── models/
    │
    ├── src/
    │
    ├── tests/
    │
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    └── teste.py

### data/

Utilizada para armazenar dados utilizados pelo projeto.

Dados gerados localmente não devem ser enviados para o GitHub quando estiverem configurados no `.gitignore`.

### docs/

Armazena a documentação do projeto.

Exemplos:

- configuração do ambiente;
- guia dos desenvolvedores;
- requisitos;
- arquitetura;
- outras documentações.

### models/

Diretório destinado aos modelos utilizados pelo sistema de Inteligência Artificial.

Modelos grandes, como arquivos `.pt`, não devem ser enviados para o GitHub caso estejam configurados no `.gitignore`.

### src/

Contém o código principal da aplicação.

### tests/

Contém os testes utilizados para verificar o funcionamento do projeto.

---

## 11. 🔒 Arquivos que não devem ser enviados ao GitHub

O projeto possui um arquivo `.gitignore`.

Ele impede que determinados arquivos sejam adicionados ao repositório.

Entre eles estão:

    .venv/
    __pycache__/
    .vscode/
    .env
    *.pt

A pasta `.venv` deve permanecer somente no computador de cada desenvolvedor.

Arquivos `.env` também não devem ser enviados ao GitHub, pois podem conter informações privadas, como chaves e configurações.

---

## 12. 🌿 Trabalhando com branches

Os integrantes não devem desenvolver diretamente na branch `main`.

Cada tarefa do Trello deverá ser desenvolvida em uma branch própria.

Primeiro atualize a `main`:

    git switch main

Depois:

    git pull

Em seguida, crie uma branch para sua tarefa:

    git switch -c nome-da-branch

Exemplo:

    git switch -c feature/deteccao-veiculos

Para uma tarefa de documentação:

    git switch -c docs/requisitos

Para configuração ou manutenção:

    git switch -c chore/configuracao-ambiente

---

## 13. 💾 Salvando alterações

Depois de realizar a tarefa, verifique o que foi alterado:

    git status

O Git mostrará os arquivos modificados, adicionados ou removidos.

Para preparar as alterações:

    git add .

Depois crie um commit:

    git commit -m "descricao da alteracao"

Exemplo:

    git commit -m "docs: adiciona guia de configuracao"

O commit representa um registro das alterações realizadas no projeto.

---

## 14. 📤 Enviando a branch para o GitHub

Depois de realizar o commit, envie a branch para o GitHub:

    git push -u origin nome-da-branch

Exemplo:

    git push -u origin docs/requisitos

Após o `push`, a branch estará disponível no GitHub.

---

## 15. 🔀 Pull Request

Depois de enviar a branch, o desenvolvedor deverá criar um Pull Request no GitHub.

O Pull Request é utilizado para solicitar que as alterações da sua branch sejam incorporadas à `main`.

Antes do merge, outro integrante deverá revisar as alterações.

O Pull Request deve informar:

- o que foi desenvolvido;
- qual tarefa do Trello está sendo realizada;
- possíveis observações;
- arquivos principais modificados.

---

## 16. 👀 Revisão

Outro integrante deverá revisar o Pull Request.

Durante a revisão, devem ser verificadas:

- funcionamento do código;
- organização dos arquivos;
- padrão de código;
- documentação;
- possíveis erros;
- relação com a tarefa do Trello.

Se estiver tudo correto, o Pull Request poderá ser aprovado.

Caso existam problemas, o responsável deverá realizar as correções solicitadas.

---

## 17. 🔀 Merge

Depois da aprovação, as alterações poderão ser incorporadas à `main` através do Merge.

O Merge junta as alterações da branch de desenvolvimento com a branch principal.

Depois do Merge, a tarefa estará oficialmente incorporada ao projeto.

---

## 18. 📋 Relação entre Trello e GitHub

O Trello será utilizado para organizar as tarefas do projeto.

O GitHub será utilizado para armazenar o código, controlar versões e realizar a colaboração entre os integrantes.

O fluxo esperado é:

    📋 Trello
        ↓
    👤 Integrante pega a tarefa
        ↓
    🌿 Cria uma branch
        ↓
    💻 Desenvolve
        ↓
    💾 Commit
        ↓
    📤 Push
        ↓
    🔀 Pull Request
        ↓
    👀 Revisão
        ↓
    🔀 Merge
        ↓
    🚀 Main
        ↓
    📋 Tarefa concluída no Trello

Sempre que possível, o Pull Request deve ser relacionado à tarefa correspondente do Trello.

---

## 19. 🔄 Atualizando o projeto

Antes de iniciar uma nova tarefa, sempre atualize sua cópia local.

Primeiro certifique-se de estar na `main`:

    git switch main

Depois:

    git pull

Em seguida crie uma nova branch para a próxima tarefa.

Isso reduz a possibilidade de trabalhar com uma versão desatualizada do projeto.

---

## 20. ⚠️ Problemas comuns

### O comando `python` não funciona

Tente:

    py --version

ou:

    py -3.12 --version

---

### O ambiente virtual não está ativo

Execute:

    .venv\Scripts\Activate.ps1

Verifique se aparece:

    (.venv)

no início do terminal.

---

### O comando `playwright` não funciona

Verifique se o ambiente virtual está ativo e execute:

    pip install -r requirements.txt

Depois:

    playwright install

---

### O Git mostra arquivos que não deveriam ser enviados

Execute:

    git status

Verifique se o arquivo ou pasta deveria estar no `.gitignore`.

Não execute `git add .` automaticamente sem verificar alterações quando houver arquivos inesperados.

---

## 21. 🆘 Se não conseguir configurar

Antes de pedir ajuda, envie para a equipe:

1. O comando que você executou;
2. A mensagem completa de erro;
3. A versão do Python;
4. O resultado de `git status`;
5. Uma captura de tela do erro, se necessário.

Não apague arquivos do projeto ou execute comandos desconhecidos tentando corrigir o problema sem consultar a equipe.

---

## ✅ Checklist final

Antes de considerar o ambiente configurado, confirme:

- [ ] Python 3.12 instalado
- [ ] Git instalado
- [ ] VS Code instalado
- [ ] Repositório clonado
- [ ] Projeto aberto no VS Code
- [ ] Ambiente `.venv` criado
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Playwright configurado
- [ ] Teste do ambiente executado
- [ ] Git funcionando corretamente
- [ ] Integrante consegue criar uma branch
- [ ] Integrante consegue realizar commit
- [ ] Integrante consegue enviar a branch para o GitHub

---

## 🚀 Pronto para desenvolver

Depois que todos os itens acima forem concluídos, o integrante estará preparado para começar suas tarefas no RoadVision.

A partir desse ponto, cada nova atividade deverá seguir o fluxo:

**Trello → Branch → Desenvolvimento → Commit → Push → Pull Request → Review → Merge → Trello.**
