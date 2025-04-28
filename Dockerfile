FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app \
    PORT=8080 \
    APP_ENV=production

EXPOSE 8080
CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "8080"]