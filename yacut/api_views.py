from http import HTTPStatus

import validators
from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .error_messages import (EMPTY_QUERY_ERROR_MESSAGE,
                             EMPTY_URL_ERROR_MESSAGE,
                             ID_NOT_FOUND_ERROR_MESSAGE,
                             URL_ERROR_MESSAGE)
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Добавляет ссылку по API."""

    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsageError(EMPTY_QUERY_ERROR_MESSAGE)

    original = data.get('url')
    if not original:
        raise InvalidAPIUsageError(EMPTY_URL_ERROR_MESSAGE)
    if not validators.url(original):
        raise InvalidAPIUsageError(URL_ERROR_MESSAGE)
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = URLMap.get_random_short(original)
    if URLMap.get(custom_id):
        raise InvalidAPIUsageError(f'Имя "{custom_id}" уже занято.')

    return jsonify(
        URLMap.save(original, custom_id).to_dict(custom_id)
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Осуществляет переадресацию."""

    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsageError(ID_NOT_FOUND_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)

    return jsonify({'url': url_map.original}), HTTPStatus.OK
