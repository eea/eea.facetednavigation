""" Versions interfaces
"""
from zope.interface import Interface
from zope import schema

class IFacetedVersion(Interface):
    """ Generate a unique key to be added to faceted queries in order to
    invalidate server proxy cache.
    """
    key = schema.TextLine(title=u'Version key')

    def __call__():
        """ Get version key
        """
