from django.db import models
from django.db.models import TextField, CharField, ImageField


class Lesson(models.Model):
    name = (
        CharField(
            max_length=200,
            verbose_name="Название урока",
            help_text="Укажите название урока.",
        ),
    )
    description = (
        TextField(verbose_name="Описание урока", help_text="Введите описание урока."),
    )
    preview = ImageField(
        verbose_name="Превью урока",
        help_text="Добавьте превью урока.",
        blank=True,
        null=True,
    )
    link_video = (
        CharField(
            max_length=200,
            verbose_name="Ссылка на видео урока",
            help_text="Добавьте ссылку на видео урока.",
            blank=True,
            null=True,
        ),
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Course(models.Model):
    name = (
        CharField(
            max_length=200,
            verbose_name="Название курса",
            help_text="Укажите название курса.",
        ),
    )
    description = (
        TextField(verbose_name="Описание курса", help_text="Введите описание курса."),
    )
    preview = ImageField(
        verbose_name="Превью курса",
        help_text="Добавьте превью курса.",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
