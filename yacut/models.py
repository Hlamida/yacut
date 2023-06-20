import re
import validators
from datetime import datetime
from random import sample

from flask import url_for

from . import db
from .constants import (
    ATTEMPTS_SHORT_GENERATE,
    ORIGINAL_LINK_LENGTH,
    REDIRECT_FUNCTION,
    VALID_SHORT_PATTERN,
    SHORT_LENGTH,
    USERS_SHORT_LENGHT,
    VALID_SHORT_SYMBOLS
)
from .error_handlers import InvalidWEBUsageError


SHORT_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXIST_MESSAGE_ERROR = 'Имя "{}" уже занято.'
SHORT_GENERATE_ERROR_MESSAGE = 'Не удалось сгенерировать короткую ссылку'
LENGTH_URL_MESSAGE_ERROR = 'Длина строки превышает {} символов'.format(ORIGINAL_LINK_LENGTH)
URL_ERROR_MESSAGE = 'Недопустимый url'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        """Метод получения объекта."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def short_generate():
        """Метод генерации короткой ссылки."""
        for _ in range(ATTEMPTS_SHORT_GENERATE):
            short = ''.join(sample(VALID_SHORT_SYMBOLS, SHORT_LENGTH))
            if not URLMap.get(short):
                return short
        raise InvalidWEBUsageError(SHORT_GENERATE_ERROR_MESSAGE)

    @staticmethod
    def save(original, short, simple_check=None):
        """Метод сохранения объекта в БД."""
        if not simple_check:
            if len(original) > ORIGINAL_LINK_LENGTH:
                raise InvalidWEBUsageError(LENGTH_URL_MESSAGE_ERROR)
            if not validators.url(original):
                raise InvalidWEBUsageError(URL_ERROR_MESSAGE)
            if short:
                if len(short) > USERS_SHORT_LENGHT:
                    raise InvalidWEBUsageError(SHORT_ERROR_MESSAGE)
                if not re.match(VALID_SHORT_PATTERN, short):
                    raise InvalidWEBUsageError(SHORT_ERROR_MESSAGE)
        if short:
            if URLMap.get(short):
                raise InvalidWEBUsageError(SHORT_EXIST_MESSAGE_ERROR.format(short))
        else:
            short = URLMap.short_generate()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def full_short(short):
        """Образует ссылку в полном виде."""
        return url_for(
            REDIRECT_FUNCTION, short=short, _external=True,
        )

    def to_dict(self):
        """Преобразует значения полей в словарь."""
        short_link = self.full_short(self.short)
        return dict(
            url=self.original,
            short_link=short_link,
        )
