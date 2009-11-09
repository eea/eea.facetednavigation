""" Caching
"""
from zope.event import notify
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.caching import InvalidateCacheEvent
from eea.facetednavigation.interfaces import IFacetedLayout
#
# Cache query
#
def cacheKeyFacetedNavigation(method, self, *args, **kwargs):
    """ Generate unique cache id for faceted query
    """
    mtool = getToolByName(self.context, 'portal_membership')
    user = mtool.getAuthenticatedMember()
    template = IFacetedLayout(self.context).layout
    return (self.context.absolute_url(1), template,
            self.request.form, self.request.get('LANGUAGE', 'en'),
            user.getUserName())

def cacheCounterKeyFacetedNavigation(method, self, *args, **kwargs):
    """ Generate unique cache id for faceted counter query
    """
    mtool = getToolByName(self.context, 'portal_membership')
    user = mtool.getAuthenticatedMember()
    return (self.context.absolute_url(1),
            self.request.form, self.request.get('LANGUAGE', 'en'),
            user.getUserName())

def invalidateFacetedCache(obj, event):
    """ Invalidate faceted navigation cache
    """
    notify(InvalidateCacheEvent(raw=True, dependencies=['eea.facetednavigation']))
