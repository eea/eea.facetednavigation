""" Search interfaces
"""
from zope.interface import Interface


class IFacetedCatalog(Interface):
    """ Faceted adapter for portal_catalog
    """
    def __call__(context, query):
        """ Call appropriate catalog
        """
