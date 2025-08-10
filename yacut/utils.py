import random
import re
import string

from settings import MAX_LEIGHT

from .models import URLMap


def get_unique_short_id(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def validate_short_id(short_id):
    """Проверяет корректность short_id."""
    if len(short_id) > MAX_LEIGHT:
        raise ValueError(f'Максимум {MAX_LEIGHT} символов')
    if not re.fullmatch(r'^[A-Za-z0-9]+$', short_id):
        raise ValueError('Только латинские буквы и цифры')
    if URLMap.query.filter_by(short=short_id).first():
        raise ValueError('Короткая ссылка уже существует')
