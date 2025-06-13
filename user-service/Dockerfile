FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências
COPY requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt

# Copia o código da aplicação
COPY . .

# Cria pasta para a base de dados SQLite
RUN mkdir -p database

# Expõe a porta do serviço
EXPOSE 5001

# Comando de arranque
CMD ["python", "app.py"]
