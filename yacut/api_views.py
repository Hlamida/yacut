from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Добавляет ссылку по API."""

    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsageError('Отсутствует тело запроса')

    original = data.get('url')
    if not original:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = URLMap.get_random_short()

    return jsonify(
        URLMap.save(original, custom_id).to_dict(custom_id)
    ), HTTPStatus.CREATED

    #return jsonify(
    #    URLMap.save(
    #        URLMap.check_url(original),
    #        URLMap.full_short(custom_id),
    #    ).to_dict()
    #), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Осуществляет переадресацию."""

    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsageError('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': url_map.original}), HTTPStatus.OK
