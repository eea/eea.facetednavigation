from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from zope.interface import implements
from interfaces import IFacetedWrapper

class FacetedWrapper(Implicit):
    """ Wrap faceted navigable container
    """
    implements(IFacetedWrapper)

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    def __call__(self, content=None):
        self.content = content
        return self.__of__(self.context)

    security.declarePublic('getFolderContents')
    def getFolderContents(self, *args, **kwargs):
        """ Override getFolderContents script
        """
        return self.content or ()

    security.declarePublic('queryCatalog')
    queryCatalog = getFolderContents

InitializeClass(FacetedWrapper)
