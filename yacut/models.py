import re
from datetime import datetime
from random import sample

from flask import flash, url_for

from . import db
from .constants import (
    QUANTITY_ATTEMPTS,
    ORIGINAL_LINK_LENGTH,
    REDIRECT_FUNCTION,
    VALID_SHORT_PATTERN,
    SHORT_LENGTH,
    USERS_SHORT_LENGHT,
    VALID_SHORT_SYMBOLS
)
from .error_handlers import InvalidUsageError, InvalidWEBUsageError
from .error_messages import (
    SHORT_ERROR_MESSAGE,
    SHORT_EXIST_MESSAGE_ERROR,
    SHORT_GENERATE_ERROR_MESSAGE
)


LENGTH_URL_MESSAGE_ERROR = 'Длина строки превышает {} символов'.format(ORIGINAL_LINK_LENGTH)


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
    def get_short(original):
        """Метод генерации и проверки новой короткой ссылки."""
        for _ in range(QUANTITY_ATTEMPTS):
            short = ''.join(sample(VALID_SHORT_SYMBOLS, SHORT_LENGTH))
            if not URLMap.get(short):
                return short
        raise InvalidWEBUsageError(SHORT_GENERATE_ERROR_MESSAGE)

    @staticmethod
    def save(original, short, form=None):
        """Метод сохранения объекта в БД."""
        if not form:
            if len(original) > ORIGINAL_LINK_LENGTH:
                raise InvalidUsageError(LENGTH_URL_MESSAGE_ERROR)
            if short:
                if len(short) > USERS_SHORT_LENGHT:
                    raise InvalidUsageError(SHORT_ERROR_MESSAGE)
                if not re.match(VALID_SHORT_PATTERN, short):
                    raise InvalidUsageError(SHORT_ERROR_MESSAGE)
        if short:
            if URLMap.get(short):
                return flash(SHORT_EXIST_MESSAGE_ERROR.format(short))
        else:
            short = URLMap.get_short(original)
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

    def to_dict(self, short):
        """Преобразует значения полей в словарь."""
        short_link = self.full_short(short)
        return dict(
            url=self.original,
            short_link=short_link,
        )
