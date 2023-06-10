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

    @staticmethod
    def check_url(cls, value):
        """Проверка корректности входного URL."""

        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('main.html', form=form)

        if not custom_id:
            custom_id = get_random_short_id()
        result_link = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )

        db.session.add(result_link)
        db.session.commit()

    @staticmethod
    def get_unique_short_id():
        pass
