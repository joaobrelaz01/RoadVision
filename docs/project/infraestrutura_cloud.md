
# Infraestrutura Cloud — RoadVision

## 1. Objetivo

Documentar a infraestrutura em nuvem utilizada pelo projeto RoadVision para execução dos componentes do sistema.

A infraestrutura foi configurada na Oracle Cloud Infrastructure (OCI), utilizando uma máquina virtual Linux acessível remotamente por SSH e com conectividade à internet.

## 2. Provedor de nuvem

* **Provedor:** Oracle Cloud Infrastructure (OCI)
* **Tipo de recurso:** Máquina Virtual (VM)
* **Nome da VM:** `roadvision-vcn`
* **Finalidade:** Ambiente de execução e testes do RoadVision

## 3. Especificações da VM

| Recurso                    | Configuração          |
| -------------------------- | ----------------------- |
| Sistema operacional        | Oracle Linux Server 9.8 |
| Arquitetura                | ARM64 (`aarch64`)     |
| Processador                | Ampere-1                |
| CPU                        | 1 vCPU                  |
| Memória RAM               | 5,5 GiB                 |
| Swap                       | 4,0 GiB                 |
| Armazenamento principal    | 30 GB                   |
| Armazenamento`/var/oled` | 15 GB                   |
| Acesso remoto              | SSH                     |

## 4. Sistema operacional

A máquina virtual utiliza o **Oracle Linux Server 9.8**, sistema operacional baseado em Linux e adequado para execução dos componentes Python utilizados pelo RoadVision.

Informações identificadas na VM:

```text
NAME="Oracle Linux Server"
VERSION="9.8"
ID="ol"
PRETTY_NAME="Oracle Linux Server 9.8"
```

A arquitetura da máquina foi identificada como:

```text
aarch64
```

correspondente à arquitetura ARM64.

## 5. Recursos computacionais

A VM possui:

* **1 vCPU**
* **CPU:** Ampere-1
* **5,5 GiB de memória RAM**
* **4,0 GiB de memória Swap**

A quantidade de CPU foi validada utilizando o comando:

```bash
nproc
```

Resultado:

```text
1
```

A memória foi validada utilizando:

```bash
free -h
```

Resultado identificado:

```text
Mem: 5.5Gi
Swap: 4.0Gi
```

## 6. Armazenamento

O armazenamento principal da VM possui 30 GB, sendo aproximadamente 20 GB utilizados e 11 GB disponíveis no momento da validação.

```text
/dev/mapper/ocivolume-root   30G   20G   11G  66% /
```

Também foi identificada uma partição adicional utilizada em:

```text
/var/oled
```

com 15 GB de capacidade.

## 7. Rede e conectividade

A VM está conectada à infraestrutura de rede da Oracle Cloud por meio da VCN configurada para o ambiente.

O hostname identificado foi:

```text
roadvision-vcn
```

O endereço IP privado identificado dentro da VM foi:

```text
10.0.0.234
```

O endereço IP público não é registrado neste documento, pois é uma informação operacional que pode sofrer alteração e não é necessária para a documentação da infraestrutura.

## 8. Acesso SSH

O acesso remoto à VM foi configurado utilizando o protocolo SSH.

A conexão foi validada a partir da máquina de desenvolvimento utilizando uma chave privada SSH.

Exemplo de acesso:

```bash
ssh -i "C:\Users\joaob\OneDrive\Desktop\Chave Cloud\ssh-key-2026-09-11 (2).key" opc@137.131.216.135
```

Após a autenticação, foi possível acessar o ambiente da VM com o usuário:

```text
opc
```

e o hostname:

```text
roadvision-vcn
```

### Status

**SSH: Funcionando**

## 9. Conectividade com a internet

A conectividade de saída da VM foi validada utilizando uma requisição HTTPS:

```bash
curl -I https://www.google.com
```

O teste retornou:

```text
HTTP/2 200
```

Esse resultado confirma que a máquina virtual possui conectividade de saída com a internet e consegue realizar requisições HTTPS.

### Status

**Internet: Funcionando**

## 10. Ambiente Python do RoadVision

A VM possui um ambiente virtual Python destinado à execução dos componentes do RoadVision.

O ambiente está localizado em:

```text
~/roadvision-test/.venv
```

Para ativação:

```bash
cd ~/roadvision-test
source .venv/bin/activate
```

A versão do Python dentro do ambiente virtual foi validada como:

```text
Python 3.12.14
```

O Python instalado no sistema operacional, fora do ambiente virtual, apresenta a versão:

```text
Python 3.9.25
```

O projeto utiliza o ambiente virtual com Python 3.12.14 para manter uma versão específica e isolada das dependências utilizadas pelo RoadVision.

## 11. Ambiente do projeto

O diretório de execução utilizado na VM é:

```text
~/roadvision-test
```

Durante a validação, foram identificados componentes relacionados ao RoadVision, incluindo:

* Ambiente virtual `.venv`;
* Scripts Python para testes e processamento;
* Arquivo de configuração de câmeras;
* Modelo `yolo11n.pt`;
* Arquivos de resultados e testes;
* Componentes relacionados à captura HLS e rastreamento.

A existência desses componentes confirma que a VM já possui um ambiente preparado para testes e execução dos componentes do projeto.

## 12. Validação da infraestrutura

Foram realizados os seguintes testes:

| Teste                                    | Resultado      |
| ---------------------------------------- | -------------- |
| VM acessível                            | ✅             |
| Acesso SSH                               | ✅ Funcionando |
| Sistema operacional identificado         | ✅             |
| Arquitetura identificada                 | ✅             |
| CPU identificada                         | ✅             |
| Memória RAM identificada                | ✅             |
| Armazenamento identificado               | ✅             |
| Conectividade com a internet             | ✅             |
| Python do sistema identificado           | ✅             |
| Ambiente virtual Python                  | ✅             |
| Python 3.12.14 no ambiente do RoadVision | ✅             |

## 13. Comandos utilizados na validação

Os principais comandos utilizados para identificar e validar a infraestrutura foram:

```bash
cat /etc/os-release
uname -m
nproc
lscpu
free -h
df -h
hostname
hostname -I
curl -I https://www.google.com
python3 --version
```

Para validação do ambiente do RoadVision:

```bash
cd ~/roadvision-test
source .venv/bin/activate
python --version
```

## 14. Critérios de aceite

### VM criada e acessível

* [X] VM criada na Oracle Cloud.
* [X] VM acessível remotamente.
* [X] Hostname `roadvision-vcn` identificado.

### Sistema operacional configurado

* [X] Oracle Linux Server 9.8 instalado e operacional.
* [X] Arquitetura ARM64 (`aarch64`) identificada.

### Acesso SSH funcionando

* [X] Acesso SSH configurado.
* [X] Conexão SSH validada com sucesso.

### Recursos da VM documentados

* [X] CPU documentada.
* [X] Memória RAM documentada.
* [X] Armazenamento documentado.
* [X] Sistema operacional documentado.
* [X] Arquitetura documentada.
* [X] Informações de rede documentadas.
* [X] Ambiente Python documentado.

## 15. Status

**Status da infraestrutura: Operacional**

A infraestrutura em nuvem do RoadVision encontra-se configurada e acessível. A máquina virtual possui sistema operacional Linux, recursos computacionais identificados, acesso SSH funcional, conectividade com a internet e ambiente Python preparado para execução dos componentes do projeto.
