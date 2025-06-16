FROM python:3.11-slim

WORKDIR /app

# Instala as dependências do serviço de health-check.
COPY requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt

COPY . .

EXPOSE 5003
CMD ["python", "app.py"]
