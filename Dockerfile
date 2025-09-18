FROM python:3.11-slim-buster
WORKDIR /app

# Копируем файл зависимостей в контейнер (обновлено: 27.06.2025, для Docker Compose)
COPY requirements.txt .
# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь остальной код проекта в контейнер
COPY . .
# Указываем команду, которая будет запускаться при старте контейнера
CMD ["python", "main.py"]