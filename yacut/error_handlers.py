from http import HTTPStatus

from flask import flash, jsonify, render_template

from . import app, db
from .forms import URLForm


class InvalidWEBUsageError(Exception):
    """Обработчик ошибок при генерации короткой ссылки."""

    def __init__(self, message):
        """Конструктор класса."""

        super().__init__()
        self.message = message


class InvalidAPIUsageError(Exception):
    """Обработчик ошибок для API."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        """Конструктор класса."""

        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Сериализация переданного сообщения об ошибке."""

        return dict(message=self.message)


@app.errorhandler(InvalidWEBUsageError)
def invalid_api_usage(error):
    """Возвращает текст ошибки во флеш-сообщении."""

    flash(error.message)
    form = URLForm()

    return render_template('index.html', form=form)


@app.errorhandler(InvalidAPIUsageError)
def invalid_api_usage(error):
    """Возвращает в ответе текст ошибки и статус-код."""

    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Обработчик ошибки 404."""

    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обработчик ошибки 500."""

    db.session.rollback()

    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
