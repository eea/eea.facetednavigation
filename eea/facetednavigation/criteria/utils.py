""" Utils
"""


def fix_string(value, _type=None):
    """Return proper value type"""
    if _type == bool and value == "1":
        return "True"
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value
