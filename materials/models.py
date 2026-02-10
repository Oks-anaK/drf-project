from django.db import models
from django.db.models import CharField, ImageField, TextField

from users.models import User


class Course(models.Model):
    name = CharField(
        max_length=200,
        verbose_name="Название курса",
        help_text="Укажите название курса.",
    )
    description = TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса.",
        blank=True,
        null=True,
    )
    preview = ImageField(
        upload_to="materials/photo_course",
        verbose_name="Превью курса",
        help_text="Добавьте превью курса.",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Добавьте владельца курса.",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = CharField(
        max_length=200,
        verbose_name="Название урока",
        help_text="Укажите название урока.",
    )
    description = TextField(
        verbose_name="Описание урока",
        help_text="Введите описание урока.",
        blank=True,
        null=True,
    )
    preview = ImageField(
        upload_to="materials/photo_lesson",
        verbose_name="Превью урока",
        help_text="Добавьте превью урока.",
        blank=True,
        null=True,
    )
    link_video = CharField(
        max_length=200,
        verbose_name="Ссылка на видео урока",
        help_text="Добавьте ссылку на видео урока.",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Введите курс.",
        related_name="lessons",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Добавьте владельца урока.",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
