FROM python:3.11-slim

WORKDIR /app

# Chrome/Chromiumのインストール
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Chromium driver パスの設定
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 開発環境用
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]