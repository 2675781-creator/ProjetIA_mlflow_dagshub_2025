FROM python:3.11-slim

WORKDIR /app

# environnement du travail
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY code/ code/
COPY test/ test/
COPY models/ models/
COPY journal_de_projet.md .
COPY requetes_enrg.jsonl .

# 8080 pour le cloud run
EXPOSE 8080 

CMD ["python", "-m", "app.main"]