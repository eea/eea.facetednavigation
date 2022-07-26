""" Versions interfaces
"""
from zope import schema
from zope.interface import Interface


class IFacetedVersion(Interface):
    """Generate a unique key to be added to faceted queries in order to
    invalidate server proxy cache.
    """

    key = schema.TextLine(title="Version key")

    def __call__():
        """Get version key"""
