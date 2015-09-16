""" Counter
"""
import operator
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from eea.facetednavigation.caching import ramcache
from eea.facetednavigation.caching import  cacheCounterKeyFacetedNavigation
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.widgets.widget import compare

class TagsCloudCounter(BrowserView):
    """ Count results per query for tags cloud widget
    """
    def query(self, cid, **kwargs):
        """ Count catalog items
        """
        # Cleanup query
        kwargs.pop('sort_on', None)
        kwargs.pop('sort_order', None)
        kwargs.pop(cid, None)
        self.request.form.pop(cid, None)

        criteria = ICriteria(self.context)
        criterion = criteria.get(cid)

        # Query catalog
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_query')

        if criterion.get('index', '') == 'Language':
            kwargs['_language_count_'] = True
        brains = handler.query(batch=False, sort=False, **kwargs)

        # Get index
        widget = criteria.widget(cid=cid)(self.context, self.request, criterion)
        vocabulary = dict((key, value) for key, value, count
                    in widget.vocabulary(oll=True) if key not in ("", "all"))

        # Count
        count = getattr(widget, 'count', lambda brains, sequence: {})
        res = count(brains, sequence=vocabulary.keys())
        res.pop("", 0)
        oll = res.pop('all', 0)

        res = res.items()
        res.sort(key=operator.itemgetter(1), reverse=True)

        maxitems = widget.maxitems
        if maxitems:
            res = res[:maxitems]
        res.sort(key=operator.itemgetter(0), cmp=compare)

        # Return a of list of three items tuples (key, label, count)
        res = [(key, vocabulary.get(key, key), value) for key, value in res]

        res.insert(0, ('all', 'All', oll))
        for item in res:
            yield item

    @ramcache(cacheCounterKeyFacetedNavigation,
              dependencies=['eea.facetednavigation'])
    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        # Calling self.index() will set cache headers for varnish
        self.index()

        cid = kwargs.pop('cid', None)
        if not cid:
            return {}

        res = self.query(cid, **kwargs)

        criteria = ICriteria(self.context)
        criterion = criteria.get(cid)
        widget = criteria.widget(cid=cid)(self.context, self.request, criterion)
        return widget(vocabulary=res)
