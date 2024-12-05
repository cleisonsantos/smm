# SMM

Este é um projeto Python que utiliza o Flask e o SQLAlchemy para gerenciar modelos de migração.

---

## Requisitos

- Python 3.8 ou superior
- Virtualenv (opcional, mas recomendado)

---

## Instalação

1. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

2. Instale as dependências:
   ```bash
    pip install -r requirements.txt
    ```

## Configuração do Banco de Dados

1. Inicialize o repositório de migrações:

    ```bash
    flask db init
    ```

2. Crie a primeira migração:

    ```bash
    flask db migrate -m "Initial migration"
    ```

3. Aplique as migrações ao banco:

    ```bash
    flask db upgrade
    ```

## Execução do Projeto

1. Inicie o servidor Flask:

    ```bash
    flask run --debug
    ```

2. Acesse o projeto no navegador:

    http://127.0.0.1:5000/
