from http import HTTPStatus
from typing import Any, Tuple

from flask import Response, redirect, render_template

from . import app
from .error_handlers import InvalidUsageError
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view() -> Tuple[Any, HTTPStatus]:
    """Отображает главную страницу."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    original_link = form.original_link.data
    return(
        render_template(
            'index.html',
            form=form,
            short_link=URLMap.full_short(
                URLMap.save(
                    original=original_link,
                    short=short,
                    form=form,
                ).short
            ),
        ),
        HTTPStatus.OK,
    )


@app.route('/<string:short>')
def redirect_view(short) -> Response:
    """Осуществляет переадресацию."""
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidUsageError('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
