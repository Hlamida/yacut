import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    ORIGINAL_LINK_LENGTH,
    REGEX_LINK_PATTERN,
    REGEX_SHORT_SYMBOLS,
    USER_LINK_LENGHT,
)


class URLForm(FlaskForm):
    """Определяет форму ввода данных."""

    original_link = URLField(
        'Введите исходную ссылку',
        validators=[
            Length(
                max=ORIGINAL_LINK_LENGTH,
                message=f'Длина строки превышает {ORIGINAL_LINK_LENGTH} символов',
            ),
            Regexp(
                REGEX_LINK_PATTERN,
                message='Недопустимый url',
            ),
            DataRequired(
                message='Обязательное поле'
            ),
        ],
    )
    custom_id = StringField(
        'Введите ваш вариант короткой ссылки',
        validators=[
            Length(
                max=USER_LINK_LENGHT,
                message=f'Длина строки превышает {USER_LINK_LENGHT} символов',
            ),
            Regexp(
                f'[{REGEX_SHORT_SYMBOLS}]',
                message='Допускаются только латинские буквы и арабские цифры',
            ),
            Optional(),
        ],
    )
    submit = SubmitField('Вжжжух!')
