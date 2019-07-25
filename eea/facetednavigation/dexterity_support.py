""" Support for dexterity content-types
"""
from Products.CMFPlone.utils import safe_unicode

import pkg_resources
import six

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    def _normalize(value):
        """ Normalize
        """
        if six.PY2 and isinstance(value, six.text_type):
            return value.encode('utf-8')
        return value
    # pyflakes
    normalize = _normalize
else:
    def normalize(value):
        """ Normalize
        """
        return safe_unicode(value)
