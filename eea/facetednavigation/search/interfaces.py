""" Search interfaces
"""
from zope.interface import Interface
try:
    from plone.app.collection.interfaces import ICollection
except ImportError:
    class ICollection(Interface):
        """ plone.app.collection not installed
        """


class IFacetedCatalog(Interface):
    """ Faceted adapter for portal_catalog
    """
    def __call__(context, query):
        """ Call appropriate catalog
        """
