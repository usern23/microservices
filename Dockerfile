# 1. Базовый образ
FROM python:3.11-slim

# 2. Установка рабочей директории
WORKDIR /app

# 3. Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем curl для healthcheck в docker-compose
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Копирование исходного кода
COPY ./src /app/src

# 5. Команда по умолчанию (может быть переопределена в docker-compose)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
