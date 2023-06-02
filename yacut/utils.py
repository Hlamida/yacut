import secrets
import string

from .constants import SHORT_LINK_LENGTH


def get_unique_short_id() -> str:
    """Формирует короткую ссылку."""

    letters_and_digits = string.ascii_letters + string.digits

    return ''.join(
        secrets.choice(
         letters_and_digits
        ) for i in range(SHORT_LINK_LENGTH)
    )
