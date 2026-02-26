from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
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


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ("stripe", "Оплата через Stripe"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
        help_text="Выберите пользователя.",
    )
    date_payment = models.DateField(
        verbose_name="Дата оплаты",
        help_text="Укажите дату оплаты.",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        related_name="payments",
        blank=True,
        null=True,
        help_text="Выберите курс (если оплачивается курс).",
    )
    lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        related_name="payments",
        blank=True,
        null=True,
        help_text="Выберите урок (если оплачивается урок).",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Укажите сумму оплаты.",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты.",
    )
    stripe_session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии Stripe",
        blank=True,
        null=True,
    )
    stripe_payment_url = models.URLField(
        max_length=500,
        verbose_name="Ссылка на оплату Stripe",
        blank=True,
        null=True,
    )

    def clean(self):
        """Валидация: должно быть заполнено либо course, либо lesson"""
        if not self.course and not self.lesson:
            raise models.ValidationError("Необходимо выбрать либо курс, либо урок.")
        if self.course and self.lesson:
            raise models.ValidationError(
                "Можно выбрать только курс или урок, не оба одновременно."
            )

    def __str__(self):
        if self.course:
            return (
                f"Платеж {self.user.email} за курс {self.course.name} - {self.amount}"
            )
        elif self.lesson:
            return (
                f"Платеж {self.user.email} за урок {self.lesson.name} - {self.amount}"
            )
        return f"Платеж {self.user.email} - {self.amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
