# PythonProject13

Django проект с использованием Docker Compose для запуска и управления сервисами.

## Требования

- Docker Desktop (или Docker Engine + Docker Compose)
- Git

## Структура проекта

Проект использует следующие сервисы:
- **web** - Django бэкенд приложение
- **db** - PostgreSQL база данных
- **redis** - Redis для кеширования и брокера сообщений Celery
- **celery** - Celery worker для выполнения асинхронных задач
- **celerybeat** - Celery Beat для планирования периодических задач

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
cd PythonProject13
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните файл `.env` необходимыми значениями:
- `SECRET_KEY` - секретный ключ Django
- `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` - настройки PostgreSQL
- `LOCATION` - URL для Redis (например: `redis://redis:6379/0`)
- Остальные переменные согласно вашему проекту

### 3. Запуск проекта

Запустите все сервисы через Docker Compose:

```bash
docker-compose up --build
```

Флаг `--build` пересоберёт образы при первом запуске.

Для запуска в фоновом режиме (detached mode):

```bash
docker-compose up -d --build
```

### 4. Применение миграций базы данных

После запуска контейнеров выполните миграции:

```bash
docker-compose exec web python manage.py migrate
```

### 5. Создание суперпользователя (опционально)

```bash
docker-compose exec web python manage.py createsuperuser
```

## Проверка работоспособности сервисов

### Web (Django)

- **URL**: http://localhost:8000
- **Проверка**: Откройте браузер и перейдите по адресу. Должна открыться главная страница Django приложения.
- **Логи**: `docker-compose logs web`

### PostgreSQL

- **Порт**: 5432
- **Проверка**: 
  ```bash
  docker-compose exec db psql -U <USER> -d <NAME> -c "SELECT version();"
  ```
  Замените `<USER>` и `<NAME>` на значения из вашего `.env` файла.
- **Логи**: `docker-compose logs db`

### Redis

- **Порт**: 6379
- **Проверка**:
  ```bash
  docker-compose exec redis redis-cli ping
  ```
  Должен вернуться ответ: `PONG`
- **Логи**: `docker-compose logs redis`

### Celery Worker

- **Проверка**:
  ```bash
  docker-compose logs celery
  ```
  Должны быть сообщения вида: `celery@<hostname> ready`
- **Статус**: `docker-compose ps celery`

### Celery Beat

- **Проверка**:
  ```bash
  docker-compose logs celerybeat
  ```
  Должны быть сообщения о планировании задач
- **Статус**: `docker-compose ps celerybeat`

## Полезные команды

### Просмотр статуса всех сервисов

```bash
docker-compose ps
```

### Просмотр логов

```bash
# Все сервисы
docker-compose logs

# Конкретный сервис
docker-compose logs web
docker-compose logs celery
docker-compose logs celerybeat
```

### Остановка сервисов

```bash
docker-compose down
```

### Остановка с удалением volumes (очистка данных БД)

```bash
docker-compose down -v
```

### Выполнение команд в контейнере

```bash
# Django команды
docker-compose exec web python manage.py <команда>

# Shell в контейнере
docker-compose exec web bash
```

### Перезапуск конкретного сервиса

```bash
docker-compose restart web
docker-compose restart celery
```

## Структура проекта

```
PythonProject13/
├── config/          # Настройки Django проекта
├── users/           # Приложение пользователей
├── materials/       # Приложение материалов
├── docker-compose.yml
├── Dockerfile
├── .env.example     # Шаблон переменных окружения
├── .env             # Файл с переменными окружения (не в git)
├── manage.py
└── README.md
```

## Решение проблем

### Docker Desktop не запущен

Убедитесь, что Docker Desktop запущен и работает:
```bash
docker --version
docker ps
```

### Проблемы с портами

Если порты заняты, измените их в `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Вместо 8000:8000
```

### Проблемы с базой данных

Проверьте переменные окружения в `.env` файле, особенно:
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST` (должен быть `db` для работы внутри Docker сети)

### Проблемы с Redis

Убедитесь, что в `.env` файле `LOCATION` указан как:
```
LOCATION=redis://redis:6379/0
```

## Разработка

Для разработки код монтируется в контейнер через volumes, поэтому изменения в коде применяются автоматически (кроме изменений в зависимостях Python, которые требуют пересборки образа).
