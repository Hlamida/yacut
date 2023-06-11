from http import HTTPStatus
from typing import Any, Tuple

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Добавляет ссылку по API."""

    try:
        data = request.get_json()
    except Exception:
        raise InvalidAPIUsageError('Отсутствует тело запроса')

    original = data.get('url')
    if not original:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    custom_id = data.get('custom_id')

    original_link = URLMap.check_url(original)
    short = URLMap.full_short(custom_id)
    url_map = URLMap.save(original_link, short)

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short) -> Tuple[Any, int]:
    """Осуществляет переадресацию."""

    original_url = URLMap.get(short)
    if not original_url:
        raise InvalidAPIUsageError('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': original_url.original}), HTTPStatus.OK
