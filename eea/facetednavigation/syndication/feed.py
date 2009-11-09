from zope import interface
from zope import component

from Products.basesyndication import interfaces as baseinterfaces
from Products.fatsyndication import adapters as fatadapters

from eea.facetednavigation.interfaces import IFacetedNavigable
try:
    from bda.feed.interfaces import ILogo
except ImportError:
    class ILogo(interface.Interface):
        """ No logo """

class FacetedFeedSource(fatadapters.BaseFeedSource):
    interface.implements(baseinterfaces.IFeedSource)
    component.adapts(IFacetedNavigable)

    def getFeedEntries(self):
        request = getattr(self.context, 'request', None)
        handler = component.getMultiAdapter((self.context, request),
                                            name=u'faceted_query')
        brains = handler.query(ajax=False)
        for brain in brains:
            doc = brain.getObject()
            if not doc:
                continue
            adapter = component.queryAdapter(doc, baseinterfaces.IFeedEntry)
            if not adapter:
                continue
            yield adapter

class FacetedFeed(fatadapters.BaseFeed):
    interface.implements(baseinterfaces.IFeed)
    component.adapts(IFacetedNavigable)

    def getImageURL(self):
        logo = component.queryAdapter(self.context, ILogo)
        if logo:
            return logo()
        return ''
