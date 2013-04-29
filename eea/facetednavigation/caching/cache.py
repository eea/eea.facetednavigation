""" Caching
"""
try:
    from eea.cache import event
    InvalidateCacheEvent = event.InvalidateCacheEvent
except ImportError:
    from eea.facetednavigation.caching.nocache import InvalidateCacheEvent

from zope.event import notify
from Products.CMFCore.utils import getToolByName
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
    kwargs.update(self.request.form)
    return (self.context.absolute_url(1), template,
            kwargs, self.request.get('LANGUAGE', 'en'),
            user.getUserName())

def cacheCounterKeyFacetedNavigation(method, self, *args, **kwargs):
    """ Generate unique cache id for faceted counter query
    """
    mtool = getToolByName(self.context, 'portal_membership')
    user = mtool.getAuthenticatedMember()
    kwargs.update(self.request.form)
    return (self.context.absolute_url(1),
            kwargs, self.request.get('LANGUAGE', 'en'),
            user.getUserName())

def cacheTreeKeyFacetedNavigation(method, self, *args, **kwargs):
    """ Generate unique cache id for faceted tree widget
    """
    mtool = getToolByName(self.context, 'portal_membership')
    user = mtool.getAuthenticatedMember()
    kwargs.update(self.request.form)
    cid = kwargs.get('cid', None)
    root = self.get_root(cid=cid) if cid else ''
    return (self.context.absolute_url(1), root,
            kwargs, self.request.get('LANGUAGE', 'en'),
            user.getUserName())

def invalidateFacetedCache(obj, evt):
    """ Invalidate faceted navigation cache
    """
    notify(InvalidateCacheEvent(raw=True,
                                dependencies=['eea.facetednavigation']))
