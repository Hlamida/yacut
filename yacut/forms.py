from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (MIN_LINK_LENGTH, REGEX_PATTERN,
                        SHORT_LINK_LENGTH)


class URLForm(FlaskForm):
    """Определяет форму ввода данных."""

    original_link = URLField(
        'Введите исходную ссылку',
        validators=[
            DataRequired(
                message='Обязательное поле'
            ),
        ],
    )
    custom_id = StringField(
        'Введите ваш вариант короткой ссылки',
        validators=[
            Length(
                MIN_LINK_LENGTH, SHORT_LINK_LENGTH,
                message=f'Длина строки превышает {SHORT_LINK_LENGTH} символов',
            ),
            Regexp(
                REGEX_PATTERN,
                message='Допускаются только латинские буквы и арабские цифры',
            ),
            Optional(),
        ],
    )
    submit = SubmitField('Вжжжух!')
