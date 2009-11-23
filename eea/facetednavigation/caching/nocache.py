"""
"""
def ramcache(get_key, dependencies=None):
    def decorator(method):
        def replacement(*args, **kwargs):
            return method(*args, **kwargs)
        return replacement
    return decorator

class InvalidateCacheEvent(object):
    """ This event will be raised if there is no cache support
    """
    def __init__(self, *args, **kwargs):
        pass
