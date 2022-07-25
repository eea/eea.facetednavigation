""" Feed
"""
from zope import component
from Products.CMFPlone.browser.syndication.adapters import FolderFeed


class FacetedFeed(FolderFeed):
    """ Feed
    """
    def _brains(self):
        """ Brains
        """
        request = getattr(self.context, 'REQUEST',
                          getattr(self.context, 'request', None))
        handler = component.getMultiAdapter((self.context, request),
                                            name=u'faceted_query')

        return handler.query(ajax=False)
