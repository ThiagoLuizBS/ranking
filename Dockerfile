FROM python:3.9-slim

WORKDIR /app

# Copiar os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código da aplicação
COPY . .

# Criar diretório de dados e garantir permissões
RUN mkdir -p /app/app/data && chmod 777 /app/app/data

# Expor a porta que o Flask vai usar
EXPOSE 5000

# Definir variáveis de ambiente
ENV FLASK_APP=app/app.py
ENV FLASK_ENV=production

# Comando para iniciar a aplicação
CMD ["python", "app/app.py"]
