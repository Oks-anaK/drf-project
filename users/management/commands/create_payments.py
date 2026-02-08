from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from users.models import User, Payments
from materials.models import Course, Lesson
from datetime import timedelta


class Command(BaseCommand):
    help = 'Создает тестовые платежи'

    def handle(self, *args, **options):
        # Получаем или создаем пользователя
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Тест',
                'last_name': 'Пользователь'
            }
        )

        # Получаем курсы и уроки
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        if not courses.exists() and not lessons.exists():
            self.stdout.write(self.style.WARNING('Нет курсов и уроков для создания платежей'))
            return

        # Создаем платежи за курсы
        if courses.exists():
            days = 0  # Начинаем с сегодня
            for course in courses[:3]:
                payment_date = timezone.now().date() - timedelta(days=days)
                Payments.objects.update_or_create(
                    user=user,
                    course=course,
                    defaults={
                        'date_payment': payment_date,
                        'amount': Decimal('5000.00'),
                        'payment_method': 'transfer'
                    }
                )
                days += 10  # Следующий платеж на 10 дней раньше
                self.stdout.write(self.style.SUCCESS(f'Создан платеж за курс: {course.name}'))

        # Создаем платежи за уроки
        if lessons.exists():
            days = 0  # Начинаем с сегодня
            for lesson in lessons[:4]:
                payment_date = timezone.now().date() - timedelta(days=days)
                Payments.objects.update_or_create(
                    user=user,
                    lesson=lesson,
                    defaults={
                        'date_payment': payment_date,
                        'amount': Decimal('500.00'),
                        'payment_method': 'cash'
                    }
                )
                days += 5  # Следующий платеж на 5 дней раньше
                self.stdout.write(self.style.SUCCESS(f'Создан платеж за урок: {lesson.name}'))
