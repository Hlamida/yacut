import re
import string


ORIGINAL_LINK_LENGTH = 2048
SHORT_LENGTH = 6
USERS_SHORT_LENGHT = 16
VALID_SHORT_SYMBOLS = string.ascii_letters + string.digits
VALID_SHORT_PATTERN = f'^[{re.escape(VALID_SHORT_SYMBOLS)}]*$'
REDIRECT_FUNCTION = 'redirect_view'
QUANTITY_ATTEMPTS = 10
