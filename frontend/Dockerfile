FROM python:3.11-slim

WORKDIR /app

COPY requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
