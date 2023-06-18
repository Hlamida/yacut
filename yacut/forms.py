from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    ORIGINAL_LINK_LENGTH,
    VALID_SHORT_PATTERN,
    USERS_SHORT_LENGHT
)

INPUT_URL_MESSAGE = 'Введите исходную ссылку'
INPUT_SHORT_MESSAGE = 'Введите ваш вариант короткой ссылки'
LENGTH_URL_MESSAGE_ERROR = 'Длина строки превышает {} символов'.format(ORIGINAL_LINK_LENGTH)
LENGTH_SHORT_MESSAGE_ERROR = 'Длина строки превышает {} символов'.format(USERS_SHORT_LENGHT)
REQUIRED_FIELD_MESSAGE_ERROR = 'Обязательное поле'
VALID_SHORT_MESSAGE_ERROR = 'Допускаются только латинские буквы и арабские цифры'
SUBMIT_PHRASE = 'Вжжжух!'


class URLForm(FlaskForm):
    """Определяет форму ввода данных."""
    original_link = URLField(
        INPUT_URL_MESSAGE,
        validators=[
            Length(
                max=ORIGINAL_LINK_LENGTH,
                message=LENGTH_URL_MESSAGE_ERROR,
            ),
            DataRequired(
                message=REQUIRED_FIELD_MESSAGE_ERROR
            ),
        ],
    )
    custom_id = StringField(
        INPUT_SHORT_MESSAGE,
        validators=[
            Length(
                max=USERS_SHORT_LENGHT,
                message=LENGTH_SHORT_MESSAGE_ERROR,
            ),
            Regexp(
                VALID_SHORT_PATTERN,
                message=VALID_SHORT_MESSAGE_ERROR,
            ),
            Optional(),
        ],
    )
    submit = SubmitField(SUBMIT_PHRASE)
