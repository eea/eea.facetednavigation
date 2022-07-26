""" Wrapper
"""
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from Acquisition import Implicit
from eea.facetednavigation.subtypes.interfaces import IFacetedWrapper
from zope.interface import implementer
from zope.traversing.adapters import DefaultTraversable
from zope.traversing.interfaces import ITraversable


@implementer(IFacetedWrapper, ITraversable)
class FacetedWrapper(Implicit):
    """Wrap faceted navigable container"""

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    def __call__(self, content=None):
        self.content = content
        return self.__of__(self.context)

    security.declarePublic("getFolderContents")

    def getFolderContents(self, *args, **kwargs):
        """Override getFolderContents script"""
        return self.content or ()

    security.declarePublic("queryCatalog")
    queryCatalog = getFolderContents

    def traverse(self, name, furtherPath):
        """Make this wrapper traversable"""
        return DefaultTraversable(self.context).traverse(name, furtherPath)


InitializeClass(FacetedWrapper)
