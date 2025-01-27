# Usar uma imagem base Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o requirements.txt e instalar as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto
COPY . /app/

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar o servidor Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
