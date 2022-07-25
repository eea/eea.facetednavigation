""" Caching module
"""
from eea.facetednavigation.caching.cache import cacheKeyFacetedNavigation
from eea.facetednavigation.caching.cache import cacheCounterKeyFacetedNavigation
from eea.facetednavigation.caching.cache import cacheTreeKeyFacetedNavigation
try:
    from eea.cache import cache, event
    ramcache = cache
    InvalidateCacheEvent = event.InvalidateCacheEvent
except ImportError:
    # Fail quiet if required cache packages are not installed in order to use
    # this package without caching
    from eea.facetednavigation.caching.nocache import ramcache
    from eea.facetednavigation.caching.nocache import InvalidateCacheEvent

__all__ = [
    cacheKeyFacetedNavigation.__name__,
    cacheCounterKeyFacetedNavigation.__name__,
    cacheTreeKeyFacetedNavigation.__name__,
    ramcache.__name__,
    InvalidateCacheEvent.__name__,
]
