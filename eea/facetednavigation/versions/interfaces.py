""" Versions interfaces
"""
from zope.interface import Interface
from zope import schema
import six


class IFacetedVersion(Interface):
    """ Generate a unique key to be added to faceted queries in order to
    invalidate server proxy cache.
    """
    key = schema.TextLine(title=u'Version key')
    key._type = (six.text_type, str)

    def __call__():
        """ Get version key
        """
