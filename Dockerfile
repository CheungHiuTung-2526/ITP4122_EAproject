FROM python:3.11-slim

# 安裝系統依賴（重要！解決 psycopg2 問題）
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]