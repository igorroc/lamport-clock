# Relógios Lógicos de Lamport com MPI

## Descrição

Este projeto implementa o algoritmo de relógio de Lamport para sincronização de relógios lógicos com comunicação causal utilizando MPI (Message Passing Interface) e a biblioteca mpi4py em Python. Este exemplo é útil para entender como funciona a sincronização de eventos em sistemas distribuídos.

## Estrutura do Projeto

```bash
lamport-clock/
├── index.py
├── README.md
└── requirements.txt
```

-   `index.py:` Contém o código principal que implementa o algoritmo de relógio de Lamport com comunicação causal.
-   `README.md:` Documentação do projeto.
-   `requirements.txt:` Arquivo com as dependências do projeto.

## Pré-requisitos

Para rodar este projeto, você precisará ter o seguinte software instalado:

-   Python 3.6 ou superior
-   MPI (MS-MPI para Windows)
-   Biblioteca mpi4py

## Instalação

### Instalação no Windows

**Passo 1: Instalar o MS-MPI**

1. Baixe e instale o MS-MPI Runtime e o MS-MPI SDK a partir do [site da Microsoft](https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi).
2. Adicione os caminhos `C:\Program Files\Microsoft MPI\Bin` e `C:\Program Files (x86)\Microsoft SDKs\MPI\Include` à variável de ambiente PATH.

**Passo 2: Instalar o mpi4py**

Abra o prompt de comando e execute o seguinte comando para instalar a biblioteca mpi4py:

```bash
pip install mpi4py
```

### Instalação no Linux

**Passo 1: Instalar o MPICH**

Abra o terminal e execute o seguinte comando para instalar o MPICH:

```bash
sudo apt-get update
sudo apt-get install -y mpich
```

**Passo 2: Instalar o mpi4py**

Abra o terminal e execute o seguinte comando para instalar a biblioteca mpi4py:

```bash
pip install mpi4py
```

## Execução

1. Clone este repositório ou baixe os arquivos para o seu computador.
2. Navegue até o diretório onde o arquivo `index.py` está salvo.
3. Execute o script utilizando `mpiexec` ou `mpirun`:

```bash
mpiexec -n 2 python lamport_clock.py
```

Substitua o número `2` pelo número de processos que deseja executar.
