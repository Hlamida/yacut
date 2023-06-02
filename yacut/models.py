from datetime import datetime

from flask import url_for

from . import db
from .constants import ORIGINAL_LINK_LENGTH, SHORT_LINK_LENGTH


class URLMap(db.Model):
    """Определяет модель БД."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LINK_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Преобразует значения полей в словарь."""

        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short=self.short, _external=True,
            ),
        )
