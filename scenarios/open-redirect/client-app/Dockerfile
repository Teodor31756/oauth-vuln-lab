# Базовый образ Python 3.10 (slim — без лишних пакетов).
FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код.
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]