from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        verbose_name="first name",
        max_length=150,
        blank=True,
        null=True,
        help_text="Введите имя.",
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=150,
        blank=True,
        null=True,
        help_text="Введите фамилию.",
    )

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту."
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите ваш номер телефона.",
    )
    town = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город, в котором вы живете.",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Добавьте свое фото.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Почта: {self.USERNAME_FIELD}."

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
