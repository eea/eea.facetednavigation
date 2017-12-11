""" Utils
"""


def fix_string(value, _type=None):
    """  Return proper value type
    """
    if _type == bool and value == u"1":
        return u"True"
    if isinstance(value, str):
        return value.decode("utf-8")
    return value
