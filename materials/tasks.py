from celery import shared_task
from django.core.mail import send_mail
from materials.models import Course
from config import settings


@shared_task
def send_info_about_updates(email, course_id):
    course = Course.objects.get(id=course_id)

    send_mail(
        subject='Обновление курса',
        message=f'Курс "{course.name}" был обновлен. Проверьте новые материалы!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
