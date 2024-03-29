from http import HTTPStatus
from typing import Any, Tuple

from flask import Response, flash, redirect, render_template

from . import app
from .error_handlers import (
    InvalidAPIUsageError,
    ShortExcistError,
)
from .forms import URLForm
from .models import URLMap


NO_ID_MESSAGE_ERROR = 'Указанный id не найден'
INDEX_PAGE = 'index.html'
SHORT_EXIST_MESSAGE_ERROR = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view() -> Tuple[Any, HTTPStatus]:
    """Отображает главную страницу."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template(INDEX_PAGE, form=form)
    short = form.custom_id.data
    try:
        url_map = URLMap.save(
            original=form.original_link.data,
            short=short,
            skip_validation=True,
        )
    except ShortExcistError:
        flash(SHORT_EXIST_MESSAGE_ERROR.format(short))
        return render_template(INDEX_PAGE, form=form)
    return(
        render_template(
            INDEX_PAGE,
            form=form,
            short_link=URLMap.full_short(url_map.short),
        ),
        HTTPStatus.OK,
    )


@app.route('/<string:short>')
def redirect_view(short) -> Response:
    """Осуществляет переадресацию."""
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsageError(NO_ID_MESSAGE_ERROR, HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
