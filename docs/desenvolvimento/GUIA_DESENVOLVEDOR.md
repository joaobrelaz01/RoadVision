git 

# 👨‍💻 Guia do Desenvolvedor — RoadVision

Este documento apresenta o fluxo padrão de desenvolvimento utilizado pela equipe do RoadVision.

O objetivo é estabelecer uma forma organizada e padronizada de trabalhar com o projeto, evitando alterações diretamente na branch principal e facilitando a colaboração entre os integrantes.

---

# 📋 1. Como funciona o desenvolvimento

O RoadVision utiliza o Trello para organizar as tarefas e o GitHub para armazenar e versionar o projeto.

Cada integrante deverá trabalhar nas tarefas atribuídas a ele no Trello.

O fluxo padrão é:

    📋 Trello
        ↓
    👤 Escolher tarefa
        ↓
    🌿 Criar branch
        ↓
    💻 Desenvolver
        ↓
    🧪 Testar
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
    ✅ Atualizar Trello

Esse processo deve ser seguido para todas as tarefas que envolvam alterações no projeto.

---

# 📋 2. Começando uma tarefa

Antes de começar uma tarefa, acesse o quadro do Trello e localize a atividade atribuída a você.

Exemplo:

    📋 Configurar ambiente de desenvolvimento

Leia atentamente:

- descrição da tarefa;
- objetivo;
- checklist;
- critérios de conclusão;
- observações deixadas pela equipe.

Antes de iniciar o desenvolvimento, mova o card para:

    🔨 Em desenvolvimento

---

# 🔄 3. Atualizar o projeto

Antes de criar uma nova branch, sempre certifique-se de que sua versão local está atualizada.

Verifique a branch atual:

    git branch

Se necessário, volte para a `main`:

    git switch main

Atualize o projeto:

    git pull

A `main` representa a versão principal e integrada do projeto.

Evite iniciar uma nova tarefa utilizando uma versão antiga da `main`.

---

# 🌿 4. Criando uma branch

Cada tarefa deve possuir sua própria branch.

Uma branch é uma ramificação independente do projeto que permite desenvolver uma alteração sem modificar diretamente a `main`.

## Padrão de nomes

Utilize um dos seguintes padrões:

    feature/nome-da-funcionalidade

    fix/nome-do-problema

    docs/nome-da-documentacao

    chore/nome-da-tarefa

### Exemplos

Nova funcionalidade:

    feature/deteccao-veiculos

Correção:

    fix/selecao-camera

Documentação:

    docs/requisitos-sistema

Configuração:

    chore/configuracao-ambiente

## Criando a branch

Depois de atualizar a `main`:

    git switch -c nome-da-branch

Exemplo:

    git switch -c feature/deteccao-veiculos

Verifique:

    git branch

A branch atual será indicada com `*`.

Exemplo:

    * feature/deteccao-veiculos
      main

---

# 💻 5. Desenvolvendo a tarefa

Com a branch criada, realize o trabalho solicitado no Trello.

O desenvolvimento deve ser realizado dentro da branch da tarefa.

Exemplo:

    feature/deteccao-veiculos

Durante o desenvolvimento:

- mantenha o código organizado;
- evite alterar arquivos que não tenham relação com a tarefa;
- siga a estrutura existente do projeto;
- utilize nomes claros para arquivos, funções e variáveis;
- mantenha a documentação atualizada quando necessário.

---

# 🧪 6. Testando as alterações

Antes de enviar qualquer alteração para o GitHub, teste o que foi desenvolvido.

Verifique se:

- o código executa corretamente;
- funcionalidades existentes continuam funcionando;
- novos recursos foram testados;
- não existem erros óbvios;
- arquivos desnecessários não foram adicionados.

Quando existirem testes automatizados, eles também deverão ser executados.

Exemplo:

    python -m pytest

Caso o projeto possua um teste específico:

    python tests/test_ambiente.py

Não envie uma alteração para revisão sem verificar se ela funciona.

---

# 🔍 7. Verificando as alterações

Antes de criar um commit, utilize:

    git status

Esse comando mostra os arquivos modificados, adicionados ou removidos.

Exemplo:

    modified: src/camera.py
    new file: src/detector.py

Também é possível visualizar exatamente o que foi alterado utilizando:

    git diff

Revise as alterações antes de continuar.

---

# 📦 8. Preparando as alterações

Depois de verificar as alterações, utilize:

    git add .

Esse comando adiciona as alterações ao próximo commit.

Se você quiser adicionar apenas um arquivo específico:

    git add caminho/do/arquivo.py

Evite adicionar arquivos desnecessários.

Antes de realizar o commit, você pode verificar novamente:

    git status

---

# 💾 9. Criando um commit

Um commit registra uma versão das alterações realizadas.

Utilize:

    git commit -m "mensagem"

As mensagens devem ser curtas e explicar claramente o que foi realizado.

## Exemplos

Nova funcionalidade:

    git commit -m "feat: adiciona deteccao de veiculos"

Correção:

    git commit -m "fix: corrige selecao da camera"

Documentação:

    git commit -m "docs: adiciona requisitos do sistema"

Configuração:

    git commit -m "chore: configura ambiente de desenvolvimento"

## Padrão recomendado

Utilizamos os seguintes prefixos:

    feat:     nova funcionalidade
    fix:      correção de problema
    docs:     documentação
    test:     testes
    chore:    configuração/manutenção
    refactor: alteração estrutural sem nova funcionalidade

---

# 📤 10. Enviando a branch para o GitHub

Depois de criar o commit, envie sua branch para o GitHub.

Utilize:

    git push -u origin nome-da-branch

Exemplo:

    git push -u origin feature/deteccao-veiculos

Depois do primeiro `push`, as alterações estarão disponíveis no GitHub.

---

# 🔀 11. Criando um Pull Request

Depois de enviar sua branch, acesse o repositório no GitHub.

O GitHub poderá apresentar a opção para criar um Pull Request.

O Pull Request representa um pedido para que suas alterações sejam revisadas e posteriormente incorporadas à `main`.

## O Pull Request deve informar

### Título

Utilize um título objetivo.

Exemplo:

    feat: adiciona deteccao de veiculos

### Descrição

Explique:

- o que foi desenvolvido;
- qual problema foi resolvido;
- quais arquivos foram alterados;
- como a alteração foi testada;
- qual tarefa do Trello está relacionada.

Exemplo:

    ## Descrição

    Implementada a primeira versão da detecção de veículos
    utilizando YOLO.

    ## Testes

    A detecção foi testada utilizando uma imagem de exemplo.

    ## Trello

    Tarefa: Implementar detecção de veículos

---

# 🔗 12. Relacionando o Pull Request ao Trello

Sempre que possível, coloque o link do Pull Request dentro do card correspondente no Trello.

Exemplo:

    📋 Implementar detecção de veículos

    GitHub:
    Pull Request #12

Isso permite relacionar:

    Tarefa
       ↓
    Desenvolvimento
       ↓
    Pull Request
       ↓
    Código

Essa relação facilita o acompanhamento do projeto.

---

# 👀 13. Code Review

Antes do Merge, outro integrante (JOÃO BRELAZ) deverá revisar o Pull Request.

Durante a revisão, devem ser analisados:

- organização do código;
- funcionamento da solução;
- possíveis erros;
- testes realizados;
- documentação;
- arquivos adicionados;
- compatibilidade com o restante do projeto.

O revisor poderá:

    ✅ Aprovar

ou:

    🔄 Solicitar alterações

Se forem solicitadas alterações, o desenvolvedor deverá realizá-las na mesma branch.

Depois:

    git add .
    git commit -m "fix: realiza ajustes solicitados na revisao"
    git push

O Pull Request será atualizado automaticamente.

---

# 🔀 14. Merge

Quando o Pull Request estiver revisado e aprovado, ele poderá ser integrado à `main`.

Esse processo é chamado de Merge.

Antes:

    main
    │
    └── feature/deteccao-veiculos

Depois:

    main
    │
    ├── feature/deteccao-veiculos
    │
    └── código integrado

Depois do Merge, a funcionalidade passa a fazer parte da versão principal do projeto.

---

# 🧹 15. Finalizando uma tarefa

Depois que o Pull Request for integrado:

1. Confirme que o Merge foi realizado;
2. Atualize sua cópia local;
3. Atualize o card do Trello;
4. Mova a tarefa para `Concluído`;
5. Adicione observações importantes no card, se necessário.

O fluxo será:

    Pull Request aprovado
            ↓
          Merge
            ↓
      Trello atualizado
            ↓
       ✅ Concluído

---

# 🔄 16. Começando outra tarefa

Depois de finalizar uma tarefa, volte para a `main`:

    git switch main

Atualize:

    git pull

Depois crie uma nova branch:

    git switch -c nome-da-nova-branch

Cada tarefa deve possuir sua própria branch.

---

# ⚠️ 17. O que NÃO fazer

## ❌ Não desenvolver diretamente na main

Evite:

    git switch main
    editar arquivos
    git add .
    git commit

A `main` deve representar uma versão integrada e estável do projeto.

---

## ❌ Não enviar a pasta .venv

A pasta `.venv` é específica de cada computador.

Ela deve permanecer no `.gitignore`.

---

## ❌ Não enviar arquivos sensíveis

Nunca envie:

    .env
    senhas
    tokens
    chaves de API
    credenciais

---

## ❌ Não apagar arquivos sem verificar

Antes de excluir ou modificar arquivos importantes, verifique se eles são utilizados por outras partes do projeto.

---

## ❌ Não utilizar mensagens de commit vagas

Evite:

    git commit -m "alterações"

    git commit -m "teste"

    git commit -m "coisas"

Prefira:

    git commit -m "fix: corrige acesso a camera"

---

# 🆘 18. Se ocorrer um problema

Não apague o projeto ou o `.git` para tentar resolver um problema.

Primeiro execute:

    git status

Depois verifique:

    git branch

Se necessário, consulte outro integrante da equipe.(JOÃO BRELAZ)

Ao pedir ajuda, informe:

1. o que você estava tentando fazer;
2. o comando executado;
3. a mensagem completa de erro;
4. a branch em que estava trabalhando;
5. o resultado de `git status`.

Uma captura de tela também pode ajudar.

---

# 📚 19. Comandos essenciais

## Verificar estado

    git status

## Ver branches

    git branch

## Criar e entrar em uma branch

    git switch -c nome-da-branch

## Trocar de branch

    git switch nome-da-branch

## Atualizar a main

    git switch main
    git pull

## Preparar alterações

    git add .

## Criar commit

    git commit -m "mensagem"

## Enviar alterações

    git push

## Baixar alterações

    git pull

## Ver alterações

    git diff

---

# 🧠 20. Resumo do fluxo

Sempre que receber uma tarefa do Trello:

    1. 📋 Pegue a tarefa
             ↓
    2. 🔨 Mova para "Em desenvolvimento"
             ↓
    3. 🌿 Atualize a main
             ↓
    4. 🌿 Crie uma branch
             ↓
    5. 💻 Desenvolva
             ↓
    6. 🧪 Teste
             ↓
    7. 🔍 Verifique as alterações
             ↓
    8. 💾 Faça o commit
             ↓
    9. 📤 Faça o push
             ↓
    10. 🔀 Crie o Pull Request
             ↓
    11. 👀 Aguarde a revisão
             ↓
    12. 🔄 Faça ajustes, se necessário
             ↓
    13. 🔀 Merge
             ↓
    14. 📋 Atualize o Trello
             ↓
    15. ✅ Tarefa concluída

---

# 🚗 RoadVision — Regra principal

O objetivo do fluxo é manter o projeto organizado e permitir que todos os integrantes trabalhem simultaneamente sem comprometer a versão principal.

Sempre que possível:

    Trello = organização das tarefas

    Git = controle de versões

    GitHub = colaboração e armazenamento do código

    Branch = ambiente isolado para uma tarefa

    Commit = registro de uma alteração

    Pull Request = solicitação de revisão

    Review = análise das alterações

    Merge = integração com a main

Seguindo esse fluxo, todos os integrantes conseguem desenvolver de forma organizada, rastreável e colaborativa.
