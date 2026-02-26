from celery import shared_task
from datetime import timedelta
from django.db import models
from django.utils import timezone
from users.models import User


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца.
    Проверяет поле last_login и устанавливает is_active=False для неактивных пользователей.
    """

    month_ago = timezone.now() - timedelta(days=30)
    
    # Находим пользователей, которые не заходили более месяца и при этом активны
    inactive_users = User.objects.filter(
        is_active=True
    ).filter(
        models.Q(last_login__lt=month_ago) | models.Q(last_login__isnull=True)
    )

    count = inactive_users.update(is_active=False)
    
    return f"Заблокировано пользователей: {count}"
