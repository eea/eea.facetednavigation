""" Wrapper
"""
from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass

from zope.traversing.interfaces import ITraversable
from zope.traversing.adapters import DefaultTraversable

from zope.interface import implements
from eea.facetednavigation.subtypes.interfaces import IFacetedWrapper


class FacetedWrapper(Implicit):
    """ Wrap faceted navigable container
    """
    implements(IFacetedWrapper, ITraversable)

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

    security.declarePublic('atctListAlbum')
    def atctListAlbum(self, *args, **kwargs):
        """ Override atctListAlbum script used by atct_album_view
        """
        return {
            'images': (),
            'folders': (),
            'subimages': (),
            'others': self.getFolderContents(),
        }

    def traverse(self, name, furtherPath):
        """ Make this wrapper traversable
        """
        return DefaultTraversable(self.context).traverse(name, furtherPath)

InitializeClass(FacetedWrapper)
