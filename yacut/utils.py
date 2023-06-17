import re


def regular_pattern(pattern):
    reg_pattern = re.escape(pattern)
    return f'[{reg_pattern}]*$'
