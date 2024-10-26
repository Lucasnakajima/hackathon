FROM python:3.9-slim

WORKDIR /app

# Instalar wget para baixar wait-for-it
RUN apt-get update && apt-get install -y wget

# Baixar wait-for-it
RUN wget -O /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usar wait-for-it para esperar o MongoDB estar pronto
CMD ["/bin/bash", "-c", "/wait-for-it.sh mongodb:27017 -t 60 -- uvicorn api:app --host 0.0.0.0 --port 8000 --reload"]
