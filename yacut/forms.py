from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length, Optional, ValidationError
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
            if not all(char.isalnum() for char in field.data):
                raise ValidationError('Только буквы и цифры')
            if URLMap.query.filter_by(short=field.data).first():
                raise ValidationError('Имя уже занято')
