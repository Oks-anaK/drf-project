from rest_framework.exceptions import ValidationError

valid_link = "youtube.com"


def validate_links(value):
    if value and not value.lower().endswith(valid_link):
        raise ValidationError("Задана недопустимая ссылка на видео.")
