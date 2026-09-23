# Code généré par Copilot de VS code, le 9.9.2026

FROM python:3.12-slim

ENV HOST=0.0.0.0 \
    PORT=8080

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8080
ENTRYPOINT ["python", "docker/entrypoint.py"]
