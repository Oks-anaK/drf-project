import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Настройка периодических задач
app.conf.beat_schedule = {
    "block-inactive-users": {
        "task": "users.tasks.block_inactive_users",
        "schedule": crontab(hour=0, minute=0),  # Каждый день в полночь (00:00)
    },
}
