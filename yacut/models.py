import re
from datetime import datetime
from random import sample

from flask import url_for

from . import db
from .constants import (ORIGINAL_LINK_LENGTH, REDIRECT_FUNCTION,
                        REGEX_LINK_PATTERN, VALID_SHORT_SYMBOLS,
                        SHORT_ID_LENGTH, USERS_SHORT_ID_LENGHT)
from .error_handlers import InvalidAPIUsageError, InvalidWEBUsageError


class URLMap(db.Model):

    MAIN = 'main'
    SHORT = 'short'

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_ID_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        """Метод получения объекта."""

        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_random_short():
        """Метод генерации и проверки новой короткой ссылки."""

        for _ in range(10):
            short = ''.join(sample(VALID_SHORT_SYMBOLS, SHORT_ID_LENGTH))
            if not URLMap.get(short):
                return short
        raise InvalidWEBUsageError('Не удалось сгенерировать короткую ссылку')

    @classmethod
    def save(cls, original, short):
        """Метод сохранения объекта в БД."""

        if not original:
            raise InvalidAPIUsageError('"url" является обязательным полем!')

        cls.check_attr(
            original, ORIGINAL_LINK_LENGTH, REGEX_LINK_PATTERN, cls.MAIN
        )
        if not short:
            short = URLMap.get_random_short()
        cls.check_attr(
            short, USERS_SHORT_ID_LENGHT, f'[{VALID_SHORT_SYMBOLS}]*$', cls.SHORT
        )
        if URLMap.get(short):
            raise InvalidAPIUsageError(f'Имя "{short}" уже занято.')
        #short = cls.full_short(short)

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()

        return url_map

    #@classmethod
    #def save(cls, original, short):
    #    """Метод сохранения объекта в БД."""
#
    #    url_map = URLMap(original=original, short=short)
    #    db.session.add(url_map)
    #    db.session.commit()
    #    return url_map


    @classmethod
    def full_short(cls, short):
        """Образует новую ссылку в полном виде."""

        return url_for(
            REDIRECT_FUNCTION, short=short, _external=True,
        )
        #URLMap.FULL_SHORT_LINK = full_short

        #return short

    #@classmethod
    #def full_short(cls, short):
    #    """Образует новую ссылку в полном виде, сохраняет её значение."""
#
    #    cls.check_attr(
    #        short, USERS_SHORT_ID_LENGHT, f'[{VALID_SHORT_SYMBOLS}]*$', cls.SHORT
    #    )
    #    if URLMap.get(short):
    #        raise InvalidAPIUsageError(f'Имя "{short}" уже занято.')
#
    #    full_short = url_for(
    #        REDIRECT_FUNCTION, short=short, _external=True,
    #    )
    #    URLMap.FULL_SHORT_LINK = full_short
#
    #    return short

    #@classmethod
    #def full_short(cls, value):
    #    """Образует новую ссылку в полном виде, сохраняет её значение."""
#
    #    cheked_short = cls.check_short_link(value)
    #    full_short = url_for(
    #        REDIRECT_FUNCTION, short=cheked_short, _external=True,
    #    )
    #    URLMap.FULL_SHORT_LINK = full_short
#
    #    return cheked_short

    def to_dict(self, short):
        """Преобразует значения полей в словарь."""

        short_link = self.full_short(short)

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

    #@classmethod
    #def check_url(cls, value):
    #    """Проверка корректности входного URL."""
#
    #    if not value:
    #        raise InvalidAPIUsageError('"url" является обязательным полем!')
    #    cls.check_attr(
    #        value, ORIGINAL_LINK_LENGTH, REGEX_LINK_PATTERN, cls.MAIN
    #    )
    #    return value

    #@classmethod
    #def check_short_link(cls, value):
    #    """Проверка короткой ссылки и генерация."""
#
    #    if not value:
    #        try:
    #            return cls.get_random_short()
    #        except Exception as error:
    #            raise InvalidAPIUsageError(error)
    #    cls.check_attr(
    #        value, USERS_SHORT_ID_LENGHT, f'[{VALID_SHORT_SYMBOLS}]*$', cls.SHORT
    #    )
    #    if URLMap.get(value):
    #        raise InvalidAPIUsageError(f'Имя "{value}" уже занято.')
    #    return value
