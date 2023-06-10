import string


ORIGINAL_LINK_LENGTH = 256
SHORT_LINK_LENGTH = 6
USER_LINK_LENGHT = 16

REGEX_LINK_PATTERN = 'http(s|)://\w+'
REGEX_SHORT_PATTERN = '[a-zA-Z0-9]+$'
REGEX_SHORT_SYMBOLS = string.ascii_letters + string.digits

REDIRECT_FUNCTION = 'redirect_view'
