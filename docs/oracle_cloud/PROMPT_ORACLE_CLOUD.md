
Estou desenvolvendo um projeto chamado RoadVision e quero configurar uma máquina virtual na Oracle Cloud para executar o sistema.

CONTEXTO DO PROJETO:
O RoadVision é um sistema de monitoramento inteligente de rodovias utilizando Visão Computacional e Inteligência Artificial.

O sistema pretende:

- Capturar imagens de câmeras rodoviárias;
- Utilizar OpenCV para processamento de imagens;
- Utilizar YOLO/Ultralytics para detecção de veículos;
- Identificar carros, motos, ônibus e caminhões;
- Contar veículos;
- Identificar o sentido do tráfego;
- Futuramente analisar fluxo e possíveis ocorrências.

TECNOLOGIAS ATUAIS:

- Python
- OpenCV
- YOLO / Ultralytics
- NumPy
- Playwright
- Git
- GitHub
- VS Code
- Oracle Cloud

REPOSITÓRIO:
GitHub:
https://github.com/joaobrelaz01/RoadVision

ESTRUTURA ATUAL DO PROJETO:

RoadVision/
├── data/
├── models/
├── src/
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── .gitignore

DESENVOLVIMENTO:
O projeto utiliza Git Flow simplificado.

Não trabalhamos diretamente na main.

Fluxo:
Trello
→ branch
→ desenvolvimento
→ commit
→ push
→ Pull Request
→ revisão
→ merge
→ main

AMBIENTE LOCAL:
Estou utilizando Windows + VS Code + PowerShell.
O projeto possui um ambiente virtual Python (.venv), que não deve ser enviado para o GitHub.

OBJETIVO DA ORACLE CLOUD:
Quero utilizar uma VM da Oracle Cloud como ambiente de execução do RoadVision.

A ideia é que:

- Meu PC seja utilizado principalmente para desenvolvimento;
- A Oracle Cloud execute o RoadVision;
- O código seja obtido através do GitHub;
- Futuramente o sistema possa ficar executando continuamente;
- O processamento das câmeras e da IA seja realizado na VM.

IMPORTANTE:
Não quero simplesmente receber todos os comandos de uma vez.

Quero que você me ensine passo a passo e espere minha confirmação após cada etapa.

Primeiro devemos verificar:

1. Qual VM Oracle Cloud estou utilizando;
2. Sistema operacional;
3. Arquitetura da VM;
4. CPU;
5. RAM;
6. Armazenamento;
7. Se a VM está dentro dos recursos gratuitos/Always Free;
8. Como acessar a VM por SSH.

Depois devemos configurar:

1. Git;
2. Python;
3. Ambiente virtual;
4. Dependências do requirements.txt;
5. Clonar o repositório RoadVision;
6. Testar o projeto;
7. Testar OpenCV;
8. Testar YOLO;
9. Testar acesso/processamento de uma câmera;
10. Somente depois configurar execução contínua.

REGRAS:

- Não alterar a main sem necessidade;
- Não enviar .venv para o GitHub;
- Não colocar senhas, tokens ou chaves privadas no código;
- Explicar o motivo de cada comando antes de executá-lo;
- Se houver erro, analisar o erro antes de sugerir outro comando;
- Considerar que estou aprendendo Linux, Git e Cloud;
- Usar linguagem simples e explicar termos técnicos.

COMECE ME PERGUNTANDO O QUE PRECISA SER VERIFICADO NA MINHA VM ORACLE CLOUD E ME GUIE PASSO A PASSO.
