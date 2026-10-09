# Infraestrutura Cloud — RoadVision

## 1. Objetivo

Registrar as características da infraestrutura utilizada para executar e testar o RoadVision na Oracle Cloud Infrastructure (OCI).

## 2. Provedor e instância

- **Provedor:** Oracle Cloud Infrastructure (OCI)
- **Nome da instância:** `roadvision-vcn`
- **Sistema operacional:** Oracle Linux 9.8
- **Arquitetura:** ARM64 (`aarch64`)
- **Shape / recursos confirmados:** 1 OCPU e aproximadamente 5,5 GiB de RAM
- **IP público utilizado para SSH:** `137.131.216.135`
- **Usuário SSH:** `opc`
- **Diretório do projeto na VM:** `/home/opc/roadvision`

> Observação: os recursos acima refletem a configuração registrada durante os testes. Confira o shape exato no painel da OCI antes de considerar este documento um inventário definitivo.

## 3. Rede e acesso remoto

- A instância está conectada a uma Virtual Cloud Network (VCN) com acesso à internet.
- O acesso administrativo remoto foi realizado por SSH na porta 22.
- A conexão SSH foi testada com sucesso a partir do terminal do Windows.
- O acesso SSH da VM ao GitHub também foi configurado por meio de uma chave dedicada para a integração com o repositório.
- **VCN, subnet, CIDR e regras completas de segurança:** não registrados com precisão neste documento; conferir no painel da OCI antes de preencher.

## 4. Ambiente de execução

- **Python:** 3.12.14
- **PyTorch:** 2.8.0+cpu
- **Ultralytics:** 8.4.131
- **Modelo de IA:** YOLO11n
- **Ambiente virtual:** `/home/opc/roadvision/.venv`
- **Arquivo do modelo:** `/home/opc/roadvision/models/yolo11n.pt`
- **Projeto:** `/home/opc/roadvision`

O modelo YOLO é executado em CPU neste ambiente. Não foi confirmada utilização de GPU/VRAM.

## 5. Testes realizados

- **Acesso SSH à VM:** aprovado.
- **Autenticação SSH da VM no GitHub:** aprovada.
- **Ambiente Python e dependências:** configurados e utilizados nos testes de inferência.
- **Conectividade de rede:** acesso externo utilizado durante a configuração e os testes.
- **Compilação de sintaxe Python:** executada com `compileall` durante a validação e o deploy.
- **GitHub Actions / CD:** workflow `.github/workflows/cd-oracle.yml` executado com status `Success`; atualiza o código da branch configurada e valida a sintaxe Python na VM.

## 6. Deploy automático

O workflow `.github/workflows/cd-oracle.yml` é acionado por `push` na branch:

`ROAD-54-task-41-avaliar-desempenho-do-processamento`

Também permite execução manual (`workflow_dispatch`). A conexão utiliza os segredos do GitHub Actions `ORACLE_HOST`, `ORACLE_USER` e `ORACLE_SSH_KEY`.

O deploy atualiza o código em `/home/opc/roadvision`. O ambiente virtual `.venv` e o modelo `models/yolo11n.pt` são mantidos na VM e não fazem parte do envio normal do Git.

## 7. Informações a confirmar no painel OCI

Para completar o inventário de infraestrutura, conferir na console da OCI:

- Shape oficial exibido para a instância.
- Nome da VCN e da subnet.
- CIDR da VCN e da subnet.
- Lista de segurança ou Network Security Group e regras de entrada/saída.
- Confirmação da regra de entrada TCP/22 limitada aos IPs necessários, sempre que possível.

Não documentar chaves privadas, senhas ou o conteúdo dos segredos do GitHub neste arquivo.

## 8. Status

A VM, o acesso SSH, o ambiente Python e o workflow de deploy foram utilizados com sucesso. A documentação registra os dados disponíveis e identifica os campos de rede que ainda precisam ser confirmados diretamente no painel OCI.
