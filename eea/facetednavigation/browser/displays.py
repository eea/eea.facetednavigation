""" Faceted views
"""
from zope import interface
from zope import component
from Products.CMFDynamicViewFTI import interfaces as cmfdynifaces
from eea.facetednavigation.interfaces import IFacetedNavigable

class ContainerDynamicViews(object):
    """ Display
    """
    interface.implements(cmfdynifaces.IDynamicallyViewable)
    component.adapts(IFacetedNavigable)

    def __init__(self, context):
        self.context = context

    def getAvailableViewMethods(self):
        """Get a list of registered view method names
        """
        return [view for view, name in self.getAvailableLayouts()]

    def getDefaultViewMethod(self):
        """Get the default view method name
        """
        return 'facetednavigation_view'

    def getAvailableLayouts(self):
        """Get the layouts registered for this object.
        """
        return (("facetednavigation_view", "Faceted View"),)
