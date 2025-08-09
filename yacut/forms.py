import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    URL,
    ValidationError,
)

from .models import URLMap


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(require_tld=True, message='Некорректный URL')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=16, message='Максимум 16 символов'),
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data:
            if not re.fullmatch(r'[A-Za-z0-9]+', field.data):
                raise ValidationError('Только латинские буквы и цифры')
            if URLMap.query.filter_by(short=field.data).first():
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
