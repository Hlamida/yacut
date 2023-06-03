import re
from http import HTTPStatus
from typing import Any, Tuple

from flask import jsonify, request

from . import app, db
from .constants import REGEX_PATTERN, USER_LINK_LENGHT
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_link() -> Tuple[Any, int]:
    """Добавляет ссылку по API."""

    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    original = data.get('url')
    if not original:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > USER_LINK_LENGHT or not re.match(
            REGEX_PATTERN, custom_id,
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage('Имя уже занято')

    else:
        custom_id = get_unique_short_id()

    result_link = URLMap(original=original, short=custom_id)
    db.session.add(result_link)
    db.session.commit()

    return jsonify(result_link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short) -> Tuple[Any, int]:
    """Осуществляет переадресацию."""

    original_url = URLMap.query.filter_by(short=short).first()
    if not original_url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': original_url.original}), HTTPStatus.OK
