""" Layout interfaces
"""
from zope import interface

class ILayoutMenuHandler(interface.Interface):
    """ Faceted layout change handler
    """

class IFacetedLayout(interface.Interface):
    """ Utility to get available layouts, current layout.
    """
