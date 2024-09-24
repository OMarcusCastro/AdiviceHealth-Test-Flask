# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos
COPY requirements.txt .

# Instale as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Exponha a porta que o Flask usará
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
