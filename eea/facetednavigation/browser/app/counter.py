""" Counter
"""
import logging
import time
import json

from zope.component import getMultiAdapter
from eea.facetednavigation.caching import ramcache
from eea.facetednavigation.caching import  cacheCounterKeyFacetedNavigation
from eea.facetednavigation.interfaces import ICriteria

logger = logging.getLogger('eea.facetednavigation.browser.app.counter')

class FacetedQueryCounter(object):
    """ Count results per query
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def query(self, cid, **kwargs):
        """ Count catalog items
        """
        # Cleanup query
        kwargs.pop('sort_on', None)
        kwargs.pop('sort_order', None)
        kwargs.pop('sort[]', None)
        kwargs.pop('sort', None)
        kwargs.pop('reversed[]', None)
        oid = '%s-operator' % cid
        operator = kwargs.pop(oid, kwargs.pop(oid + '[]', None))

        if not operator or operator != 'and':
            kwargs.pop(cid, None)
            self.request.form.pop(cid, None)
            # jQuery >= 1.4 adds type to params keys
            # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
            # Let's fix this
            kwargs.pop(cid + '[]', None)
            self.request.form.pop(cid + '[]', None)

        criteria = ICriteria(self.context)
        criterion = criteria.get(cid)

        start = time.time()
        # Query catalog
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_query')

        if criterion.get('index', '') == 'Language':
            kwargs['_language_count_'] = True
        brains = handler.query(batch=False, sort=False, **kwargs)

        # Get index
        widget = criteria.widget(cid=cid)(self.context, self.request, criterion)
        count = getattr(widget, 'count', lambda brains: {})
        res = count(brains)
        logger.debug('Benchmark %s: %s', cid, time.time() - start)
        return res

    @ramcache(cacheCounterKeyFacetedNavigation,
              dependencies=['eea.facetednavigation'])
    def __call__(self, *args, **kwargs):
        # Calling self.index() will set cache headers for varnish
        self.index()

        if self.request:
            kwargs.update(self.request.form)
            self.request.response.setHeader('Content-Type',
                                            'application/json; charset=utf-8')

        cid = kwargs.pop('cid', None)
        if not cid:
            return {}

        res = self.query(cid, **kwargs)
        return json.dumps(res)
