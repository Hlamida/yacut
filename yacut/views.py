from http import HTTPStatus
from typing import Any, Tuple

from flask import Response, flash, redirect, render_template

from . import app
from .error_handlers import InvalidAPIUsageError, InvalidWEBUsageError
from .forms import URLForm
from .models import URLMap
from .constants import REDIRECT_FUNCTION


@app.route('/', methods=['GET', 'POST'])
def index_view() -> Tuple[Any, HTTPStatus]:
    """Отображает главную страницу."""

    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    original_link = form.original_link.data

    if URLMap.get(custom_id):
        raise InvalidWEBUsageError(f'Имя {custom_id} уже занято!')

    if not custom_id:
        custom_id = URLMap.full_short(value=None)

    URLMap.save(
        original=original_link,
        short=custom_id,
    )
    context = {
        'form': form,
        'short': custom_id,
        'REDIRECT_FUNCTION': REDIRECT_FUNCTION,
        'FULL_SHORT_LINK': URLMap.FULL_SHORT_LINK,
    }

    return(
        render_template('index.html', **context),
        HTTPStatus.OK,
    )


@app.route('/<string:short>')
def redirect_view(short) -> Response:
    """Осуществляет переадресацию."""

    original_url = URLMap.get(short)
    if not original_url:
        raise InvalidAPIUsageError('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return redirect(original_url.original)
