from http import HTTPStatus
from typing import Any, Tuple

from flask import Response, redirect, render_template

from . import app
from .error_handlers import InvalidAPIUsageError
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view() -> Tuple[Any, HTTPStatus]:
    """Отображает главную страницу."""

    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    original_link = form.original_link.data

    url_map = URLMap.save(
        original=original_link,
        short=custom_id,
    )

    return(
        render_template(
            'index.html',
            form=form,
            FULL_SHORT_LINK=URLMap.full_short(url_map.short),
        ),
        HTTPStatus.OK,
    )


@app.route('/<string:short>')
def redirect_view(short) -> Response:
    """Осуществляет переадресацию."""

    original_url = URLMap.get(short)
    if not original_url:
        raise InvalidAPIUsageError('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return redirect(original_url.original)
