import string

from .utils import regular_pattern

ORIGINAL_LINK_LENGTH = 2048
SHORT_LENGTH = 6
USERS_SHORT_ID_LENGHT = 16
VALID_SHORT_SYMBOLS = string.ascii_letters + string.digits
REG_PATTERN = regular_pattern(VALID_SHORT_SYMBOLS)
REDIRECT_FUNCTION = 'redirect_view'
COUNT_ORIGINAL = 10
