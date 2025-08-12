from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    URL,
    ValidationError,
)
from settings import MAX_LEIGHT
from .utils import validate_short_id


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
            Length(max=MAX_LEIGHT, message=f'Максимум {MAX_LEIGHT} символов')
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data:
            error = validate_short_id(field.data)
            if error:
                raise ValidationError(error)
