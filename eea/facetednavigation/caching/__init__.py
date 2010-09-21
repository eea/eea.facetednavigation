""" Caching module
"""
try:
    from eea.cache import cache as ramcache
    from lovely.memcached.event import InvalidateCacheEvent
except ImportError:
    # Fail quiet if required cache packages are not installed in order to use
    # this package without caching
    from nocache import ramcache
    from nocache import InvalidateCacheEvent

try:
    # Plone 4+
    from zope.lifecycleevent.interfaces import IObjectModifiedEvent
except ImportError:
    #BBB Plone < 4
    from zope.app.container.interfaces import IObjectModifiedEvent

from cache import cacheKeyFacetedNavigation
from cache import cacheCounterKeyFacetedNavigation

