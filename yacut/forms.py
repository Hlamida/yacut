from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (ORIGINAL_LINK_LENGTH,
                        REG_PATTERN, USERS_SHORT_ID_LENGHT)


class URLForm(FlaskForm):
    """Определяет форму ввода данных."""
    original_link = URLField(
        'Введите исходную ссылку',
        validators=[
            Length(
                max=ORIGINAL_LINK_LENGTH,
                message=f'''
                Длина строки превышает {ORIGINAL_LINK_LENGTH} символов
                ''',
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
                max=USERS_SHORT_ID_LENGHT,
                message=f'Длина строки превышает {USERS_SHORT_ID_LENGHT} символов',
            ),
            Regexp(
                REG_PATTERN,
                message='Допускаются только латинские буквы и арабские цифры',
            ),
            Optional(),
        ],
    )
    submit = SubmitField('Вжжжух!')
