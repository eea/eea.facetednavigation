""" Utils
"""


def fix_string(value):
    """  Return proper value type
    """
    if isinstance(value, str):
        return value.decode("utf-8")
    return value
