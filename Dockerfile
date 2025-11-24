FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY code/ code/
COPY test/ test/
COPY models/ models/
COPY journal_de_projet.md .
COPY requetes_enrg.jsonl .

EXPOSE 8000

CMD ["python", "-m", "app.main"]