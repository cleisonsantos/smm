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
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
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

---

## Executando com Docker/Podman

### Requisitos
- Docker ou Podman instalado na máquina.

### Passo a Passo

1. **Crie a imagem Docker**

   Para Docker:
   ```bash
   docker-compose build
   ```

   Para Podman:
   ```bash
   podman-compose build
   ```

2. **Suba os contêineres**

   Para Docker:
   ```bash
   docker-compose up
   ```

   Para Podman:
   ```bash
   podman-compose up
   ```

3. **Acesse o projeto**

   Após os contêineres estarem rodando, acesse no navegador:
   ```
   http://localhost:5000
   ```

4. **Executar migrações no SQLite**

   Após subir os contêineres, entre no terminal do contêiner Flask para executar as migrações:

   Para Docker:
   ```bash
   docker exec -it flask-app bash
   ```

   Para Podman:
   ```bash
   podman exec -it flask-app bash
   ```

   Dentro do contêiner, execute:
   ```bash
   flask db upgrade
   ```

5. **Parar os contêineres**

   Para Docker:
   ```bash
   docker-compose down
   ```

   Para Podman:
   ```bash
   podman-compose down
   ```

---
