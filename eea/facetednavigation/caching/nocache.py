""" When cache is not supported
"""
def ramcache(get_key, dependencies=None):
    """ RAM cache
    """
    def decorator(method):
        """ Decorator
        """
        def replacement(*args, **kwargs):
            """ Replacement method
            """
            return method(*args, **kwargs)
        return replacement
    return decorator

class InvalidateCacheEvent(object):
    """ This event will be raised if there is no cache support
    """
    def __init__(self, *args, **kwargs):
        pass
