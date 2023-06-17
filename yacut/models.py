import re
from datetime import datetime
from random import sample

from flask import flash, render_template, url_for

from . import db
from .constants import (COUNT_ORIGINAL,
                        ORIGINAL_LINK_LENGTH,
                        REDIRECT_FUNCTION,
                        REG_PATTERN,
                        SHORT_LENGTH,
                        USERS_SHORT_ID_LENGHT,
                        VALID_SHORT_SYMBOLS)
from .error_handlers import InvalidAPIUsageError, InvalidWEBUsageError
from .error_messages import (SHORT_ERROR_MESSAGE, SHORT_GENERATE_ERROR_MESSAGE)
from .forms import URLForm


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
    def get_random_short(original):
        """Метод генерации и проверки новой короткой ссылки."""
        for _ in range(COUNT_ORIGINAL):
            short = ''.join(sample(VALID_SHORT_SYMBOLS, SHORT_LENGTH))
            if not URLMap.get(short):
                return short
        raise InvalidWEBUsageError(SHORT_GENERATE_ERROR_MESSAGE)

    @staticmethod
    def save(original, short):
        """Метод сохранения объекта в БД."""
        form = URLForm()
        if len(original) > ORIGINAL_LINK_LENGTH:
            raise InvalidAPIUsageError(f'''
                Длина строки превышает {ORIGINAL_LINK_LENGTH} символов
                ''',)
        if short:
            if not len(short) <= USERS_SHORT_ID_LENGHT:
                raise InvalidAPIUsageError(SHORT_ERROR_MESSAGE)
            if not re.match(REG_PATTERN, short):
                raise InvalidAPIUsageError(SHORT_ERROR_MESSAGE)
            if URLMap.get(short):
                flash(f'Имя {short} уже занято!')
                return render_template('index.html', form=form)
        else:
            short = URLMap.get_random_short(original)
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
