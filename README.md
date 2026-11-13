# Controle Financeiro

Projeto desenvolvido em Python com MongoDB para gerenciamento de receitas e despesas pessoais.

## Sobre o projeto

O Controle Financeiro permite registrar movimentações financeiras, consultar lançamentos, organizar receitas e despesas por categoria e acompanhar o saldo disponível.

O projeto foi desenvolvido como atividade do 4º bimestre da disciplina de Banco de Dados.

## Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento.
- **MongoDB Atlas:** banco de dados não relacional utilizado para armazenar os lançamentos.
- **PyMongo:** biblioteca responsável pela comunicação entre Python e MongoDB.
- **Python-dotenv:** biblioteca utilizada para carregar variáveis de ambiente.

## Funcionalidades

- Cadastro de receitas e despesas.
- Consulta dos últimos 30 lançamentos.
- Resumo financeiro agrupado por categoria.
- Cálculo automático do saldo.
- Filtro de lançamentos por mês e ano.
- Exclusão de lançamentos com confirmação.
- Exportação dos lançamentos para arquivo CSV.

## Estrutura do projeto

```text
ControleFinanceiro/
│
├── p05_financas/
│   ├── __init__.py
│   └── main.py
│
├── conexao.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd ControleFinanceiro
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Configurar o MongoDB

Crie um arquivo `.env` na pasta principal do projeto e configure sua URI de conexão:

```env
MONGO_URI=sua_string_de_conexao
```

O banco de dados utilizado pelo projeto é `laboratorio_python`, e a coleção de lançamentos é `lancamentos_p05`.

### 6. Executar o programa

Na pasta principal, execute:

```bash
python -m p05_financas.main
```

## Organização financeira

Os valores monetários são armazenados em centavos para evitar problemas de precisão em operações financeiras.

O resumo financeiro utiliza operações de agregação do MongoDB, como `$group`, `$sum` e `$sort`.

## Autores

Gabriel Santos Ribeiro,
Nicolas do Vale Oliveira Moreira,
Ricardo Santos de Morais.

**Projeto 05 — Controle Financeiro | 4º Bimestre**