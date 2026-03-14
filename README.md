# PythonProject13

Django проект с использованием Docker Compose для локальной разработки и автоматическим деплоем на удаленный сервер через GitHub Actions.

## Требования

- Docker Desktop (для локальной разработки)
- Git

## Локальная разработка (Docker Compose)

### Быстрый старт

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Oks-anaK/drf-project.git
cd drf-project
```

2. Создайте `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Заполните переменные в `.env`:
- `SECRET_KEY` - секретный ключ Django
- `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` - настройки PostgreSQL
- `LOCATION=redis://redis:6379/0` - Redis для Docker
- Остальные переменные согласно проекту

4. Запустите проект:
```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
```

5. Приложение доступно: http://localhost:8000

### Полезные команды

```bash
# Статус сервисов
docker-compose ps

# Логи
docker-compose logs web

# Остановка
docker-compose down

# Django команды
docker-compose exec web python manage.py <команда>
```

---

## Настройка удаленного сервера (продакшн)

> **Важно**: Для продакшена используется настройка без Docker. Переменные окружения отличаются от Docker-версии (см. ниже).

### Основные шаги

1. **Установка пакетов:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git nginx curl ufw postgresql postgresql-contrib libpq-dev
```

2. **Настройка Firewall:**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

3. **Безопасность SSH:**
```bash
sudo nano /etc/ssh/sshd_config
# Установи: PasswordAuthentication no, PubkeyAuthentication yes, PermitRootLogin no
sudo systemctl restart ssh
```

4. **Создание пользователя deploy:**
```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
su - deploy
```

5. **Установка Poetry:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

6. **Клонирование проекта:**
```bash
mkdir -p ~/apps
cd ~/apps
git clone https://github.com/Oks-anaK/drf-project.git
cd drf-project
git checkout develop
```

7. **Настройка зависимостей:**
```bash
poetry config virtualenvs.in-project true
poetry install --only main --no-root
poetry add gunicorn
```

8. **PostgreSQL:**
```bash
sudo -u postgres psql
# CREATE DATABASE db_name;
# CREATE USER db_user WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE db_name TO db_user;
```

9. **Создание .env на сервере:**
```bash
nano ~/apps/drf-project/.env
```

**Важные отличия от Docker:**
- `HOST=localhost` (не `db`!)
- `DB_USER=db_user` (не `USER` - чтобы избежать конфликта с системной переменной!)
- `LOCATION=redis://127.0.0.1:6379/0` (не `redis://redis:6379/0`!)
- `ALLOWED_HOSTS=SERVER_IP,yourdomain.com`
- `DEBUG=0`

10. **Миграции и статика:**
```bash
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
```

11. **Gunicorn + Systemd:**
```bash
sudo nano /etc/systemd/system/drf-project.service
```

```ini
[Unit]
Description=Gunicorn via Poetry for drf-project
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/home/deploy/apps/drf-project
EnvironmentFile=/home/deploy/apps/drf-project/.env

ExecStart=/home/deploy/apps/drf-project/.venv/bin/gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 3 \
  --timeout 60

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable drf-project
sudo systemctl start drf-project
```

12. **Nginx:**
```bash
sudo nano /etc/nginx/sites-available/drf-project
```

```nginx
server {
    listen 80;
    server_name SERVER_IP yourdomain.com;

    location /static/ {
        alias /home/deploy/apps/drf-project/static/;
    }

    location /media/ {
        alias /home/deploy/apps/drf-project/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/drf-project /etc/nginx/sites-enabled/drf-project
sudo nginx -t
sudo systemctl reload nginx
```

13. **Права доступа:**
```bash
sudo chmod 755 /home/deploy
sudo chown -R deploy:www-data /home/deploy/apps/drf-project/static
sudo chmod -R 755 /home/deploy/apps/drf-project/static
```

14. **Sudo без пароля для deploy:**
```bash
sudo visudo
# Добавьте: deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart drf-project, /usr/bin/systemctl reload nginx
```

15. **SSH-ключи для GitHub Actions:**
```bash
sudo su - deploy
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Вставьте публичный ключ с ноутбука
chmod 600 ~/.ssh/authorized_keys
```

---

## GitHub Actions Workflow

### Настройка

1. **Добавьте Secrets в GitHub:**
   - Settings → Secrets and variables → Actions
   - `SSH_HOST` - IP сервера
   - `SSH_USER` - deploy
   - `SSH_PRIVATE_KEY` - приватный ключ (весь файл с BEGIN/END)
   - `SSH_PORT` - 22 (опционально)

### Как работает

- При push в `main`/`master`/`develop` запускается workflow
- Сначала выполняются тесты
- Если тесты успешны → автоматический деплой на сервер
- Если тесты упали → деплой не выполняется

### Что делает деплой

1. Подключается по SSH
2. `git stash` → `git checkout develop` → `git pull`
3. Обновляет зависимости (`poetry install`)
4. Применяет миграции (`migrate`)
5. Собирает статику (`collectstatic`)
6. Перезапускает Gunicorn и Nginx

Workflow файл: `.github/workflows/ci-cd.yml`

---

## Ручное обновление на сервере

```bash
ssh deploy@SERVER_IP
cd ~/apps/drf-project
git pull
export PATH="$HOME/.local/bin:$PATH"
poetry install --only main --no-root
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
sudo systemctl restart drf-project
```

---

## Тестирование

```bash
# Локально (Docker)
docker-compose exec web python manage.py test

# Локально (без Docker)
poetry run python manage.py test

# В GitHub Actions - автоматически при push
```

---

## Структура проекта

```
PythonProject13/
├── config/              # Настройки Django
├── users/               # Приложение пользователей
├── materials/           # Приложение материалов
├── .github/
│   └── workflows/
│       └── ci-cd.yml    # GitHub Actions
├── docker-compose.yml   # Docker для разработки
├── .env.example         # Шаблон переменных окружения
└── README.md
```

---

## Важные замечания

- **Для продакшена**: Используй `DB_USER` вместо `USER` в `settings.py` (конфликт с системной переменной)
- **Переменные окружения**: На сервере `HOST=localhost`, в Docker `HOST=db`
- **Redis**: На сервере `redis://127.0.0.1:6379/0`, в Docker `redis://redis:6379/0`
