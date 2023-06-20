from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError, InvalidWEBUsageError
from .models import URLMap

EMPTY_QUERY_ERROR_MESSAGE = 'Отсутствует тело запроса'
EMPTY_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
ID_NOT_FOUND_ERROR_MESSAGE = 'Указанный id не найден'
URL_ERROR_MESSAGE = 'Недопустимый url'
SHORT_EXIST_MESSAGE_ERROR = 'Имя "{}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Добавляет ссылку по API."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsageError(EMPTY_QUERY_ERROR_MESSAGE)
    original = data.get('url')
    if not original:
        raise InvalidAPIUsageError(EMPTY_URL_ERROR_MESSAGE)
    custom_id = data.get('custom_id')
    try:
        url_map = URLMap.save(original, custom_id)
    except InvalidWEBUsageError as error:
        if 'занято' in str(error):
            raise InvalidAPIUsageError(
                SHORT_EXIST_MESSAGE_ERROR.format(custom_id)
            )
        raise InvalidAPIUsageError(str(error))
    return jsonify(
        url_map.to_dict()
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Осуществляет переадресацию."""
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsageError(
            ID_NOT_FOUND_ERROR_MESSAGE, HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK
