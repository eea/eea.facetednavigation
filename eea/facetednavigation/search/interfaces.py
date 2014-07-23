""" Search interfaces
"""
from zope.interface import Interface
try:
    from plone.app.collection import interfaces
    ICollection = interfaces.ICollection
except (ImportError, AttributeError):
    class ICollection(Interface):
        """ plone.app.collection not installed
        """


class IFacetedCatalog(Interface):
    """ Faceted adapter for portal_catalog
    """
    def __call__(context, query):
        """ Call appropriate catalog
        """
