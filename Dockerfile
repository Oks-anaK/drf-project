FROM python:3.12

WORKDIR /code

# Установка Poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --only=main --no-root && \
    pip cache purge

# Копирование всего кода проекта
COPY . .

# Команда по умолчанию (переопределяется в docker-compose.yml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
