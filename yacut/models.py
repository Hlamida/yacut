import re
from enum import Enum
from random import sample
from datetime import datetime

from flask import url_for

from .constants import (
    ORIGINAL_LINK_LENGTH,
    SHORT_LINK_LENGTH,
    REDIRECT_FUNCTION,
    REGEX_LINK_PATTERN,
    REGEX_SHORT_PATTERN,
    REGEX_SHORT_SYMBOLS,
    USER_LINK_LENGHT,
)
from . import db
from .error_handlers import InvalidAPIUsageError, InvalidWEBUsageError


class URLMap(db.Model):

    MAIN = 'main'
    SHORT = 'short'
    FULL_SHORT_LINK = ''

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LINK_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.original}'

    @staticmethod
    def get(short_id):
        """Метод получения объекта."""

        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_random_short_id():
        """Метод генерации и проверки новой короткой ссылки."""

        short = ''.join(sample(REGEX_SHORT_SYMBOLS, SHORT_LINK_LENGTH))
        if not URLMap.get(short):
            return short
        raise InvalidWEBUsageError('Не удалось сгенерировать короткую ссылку')

    @classmethod
    def save(cls, original, short):
        """Метод сохранения объекта в БД."""

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def full_short(value):
        full_short = url_for(
            REDIRECT_FUNCTION, short=value, _external=True,
        )
        URLMap.FULL_SHORT_LINK = full_short
        return full_short


    def to_dict(self):
        """Преобразует значения полей в словарь."""

        short_link = URLMap.FULL_SHORT_LINK

        return dict(
            url=self.original,
            short_link=short_link,
        )

    @classmethod
    def check_attr(cls, value, end, pattern, item):
        """Проверка корректности параметра."""

        if (not isinstance(value, str) or not len(value) <= end or
                not re.match(pattern, value)):
            if item == cls.MAIN:
                raise InvalidAPIUsageError('Недопустимый url')
            else:
                raise InvalidAPIUsageError('Указано недопустимое имя для короткой ссылки')

    @classmethod
    def check_url(cls, value):
        """Проверка корректности входного URL."""

        if not value:
            raise InvalidAPIUsageError('"url" является обязательным полем!')
        cls.check_attr(
            value, ORIGINAL_LINK_LENGTH, REGEX_LINK_PATTERN, cls.MAIN
        )
        return value

    @classmethod
    def check_short_link(cls, value):
        """Проверка короткой ссылки и генерация."""

        if not value:
            try:
                random_short_id = cls.get_random_short_id()
                cls.full_short(random_short_id)
                return random_short_id
            except Exception as error:
                raise InvalidAPIUsageError(error)
        cls.check_attr(
            value, USER_LINK_LENGHT, REGEX_SHORT_PATTERN, cls.SHORT
        )
        if URLMap.get(value):
            raise InvalidAPIUsageError(f'Имя "{value}" уже занято.')
        cls.full_short(value)
        return value
