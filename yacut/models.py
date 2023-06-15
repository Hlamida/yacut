import re
from datetime import datetime
from random import sample

from flask import url_for

from . import db
from .constants import (ORIGINAL_LINK_LENGTH,
                        REDIRECT_FUNCTION,
                        SHORT_ID_LENGTH,
                        USERS_SHORT_ID_LENGHT,
                        VALID_SHORT_SYMBOLS)
from .error_handlers import InvalidAPIUsageError, InvalidWEBUsageError
from .error_messages import (EMPTY_URL_ERROR_MESSAGE,
                             SHORT_ERROR_MESSAGE,
                             SHORT_GENERATE_ERROR_MESSAGE)


class URLMap(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_ID_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        """Метод получения объекта."""

        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_random_short(original):
        """Метод генерации и проверки новой короткой ссылки."""

        count_original = URLMap.query.filter_by(original=original).count()

        for _ in range(count_original + 1):
            short = ''.join(sample(VALID_SHORT_SYMBOLS, SHORT_ID_LENGTH))
            if not URLMap.get(short):
                return short
        raise InvalidWEBUsageError(SHORT_GENERATE_ERROR_MESSAGE)

    @staticmethod
    def save(original, short):
        """Метод сохранения объекта в БД."""

        if not original:
            raise InvalidAPIUsageError(EMPTY_URL_ERROR_MESSAGE)

        if not short:
            short = URLMap.get_random_short(original)
        URLMap.check_attr(
            short, USERS_SHORT_ID_LENGHT, VALID_SHORT_SYMBOLS, SHORT_ERROR_MESSAGE,
        )

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()

        return url_map

    @staticmethod
    def full_short(short):
        """Образует новую ссылку в полном виде."""

        return url_for(
            REDIRECT_FUNCTION, short=short, _external=True,
        )

    def to_dict(self, short):
        """Преобразует значения полей в словарь."""

        short_link = self.full_short(short)

        return dict(
            url=self.original,
            short_link=short_link,
        )

    @staticmethod
    def check_attr(value, end, pattern, item):
        """Проверка корректности параметра."""
        reg_pattern = re.escape(pattern)
        regular = f'[{reg_pattern}]*$'

        if not len(value) <= end:
            raise InvalidAPIUsageError(item)
        if not re.match(regular, value):
            raise InvalidAPIUsageError(item)
