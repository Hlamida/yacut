from http import HTTPStatus

import validators
from flask import jsonify, request

from . import app
from .error_handlers import InvalidUsageError
from .models import URLMap

EMPTY_QUERY_ERROR_MESSAGE = 'Отсутствует тело запроса'
EMPTY_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
ID_NOT_FOUND_ERROR_MESSAGE = 'Указанный id не найден'
URL_ERROR_MESSAGE = 'Недопустимый url'
SHORT_EXIST_MESSAGE_ERROR = 'Имя {} уже занято.'


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Добавляет ссылку по API."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidUsageError(EMPTY_QUERY_ERROR_MESSAGE)
    original = data.get('url')
    if not original:
        raise InvalidUsageError(EMPTY_URL_ERROR_MESSAGE)
    if not validators.url(original):
        raise InvalidUsageError(URL_ERROR_MESSAGE)
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = URLMap.get_short(original)
    if URLMap.get(custom_id):
        raise InvalidUsageError(SHORT_EXIST_MESSAGE_ERROR.format(custom_id))
    return jsonify(
        URLMap.save(original, custom_id).to_dict(custom_id)
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Осуществляет переадресацию."""
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidUsageError(ID_NOT_FOUND_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
