FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências
COPY requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta do frontend
EXPOSE 5000

# Comando de arranque
CMD ["python", "app.py"]
