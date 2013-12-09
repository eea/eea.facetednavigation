""" Support for dexterity content-types
"""

import pkg_resources
try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    def _normalize(value):
        """ Normalize
        """
        if isinstance(value, unicode):
            return value.encode('utf-8')
        else:
            return value
    #pyflakes
    normalize = _normalize
else:
    def normalize(value):
        """ Normalize
        """
        if isinstance(value, str):
            return value.decode('utf-8')
        else:
            return value
