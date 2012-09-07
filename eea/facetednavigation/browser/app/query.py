""" Faceted query
"""
import logging
from types import GeneratorType
from zope.component import queryMultiAdapter
from zope.component import getUtility
from zope.component import queryAdapter

from Products.CMFPlone.utils import safeToInt
from Products.CMFPlone.PloneBatch import Batch

from eea.facetednavigation.caching import ramcache
from eea.facetednavigation.caching import cacheKeyFacetedNavigation
from eea.facetednavigation.interfaces import IFacetedLayout
from eea.facetednavigation.interfaces import IFacetedCatalog
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import ILanguageWidgetAdapter
from eea.facetednavigation.interfaces import IFacetedWrapper
from eea.facetednavigation.interfaces import IWidgetFilterBrains

logger = logging.getLogger('eea.facetednavigation.browser.app.query')

class FacetedQueryHandler(object):
    """ Faceted Query
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def macros(self, name='content-core'):
        """ Return macro from default layout
        """
        return IFacetedLayout(self.context).get_macro(macro=name)

    @property
    def language(self):
        """ Get context language
        """
        lang = getattr(self.context, 'getLanguage', None)
        if lang:
            return lang()
        return self.request.get('LANGUAGE', '')

    @property
    def default_criteria(self):
        """ Return default criteria
        """
        query = {}
        criteria = queryAdapter(self.context, ICriteria)
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)
            widget = widget(self.context, self.request, criterion)
            default = widget.default
            if not default:
                continue
            query[cid.encode('utf-8')] = default
        return query

    def get_context(self, content=None):
        """ Return context
        """
        wrapper = queryAdapter(self.context, IFacetedWrapper)
        if not wrapper:
            return self.context
        return wrapper(content)

    def criteria(self, sort=True, **kwargs):
        """ Process catalog query
        """
        if self.request:
            kwargs.update(self.request.form)

        # jQuery >= 1.4 adds type to params keys
        # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
        # Let's fix this
        kwargs = dict((key.replace('[]', ''), val)
                      for key, val in kwargs.items())

        logger.debug("REQUEST: %r", kwargs)

        # Generate the catalog query
        criteria = ICriteria(self.context)
        query = {}
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)
            widget = widget(self.context, self.request, criterion)

            query.update(widget.query(kwargs))

            # Handle language widgets
            if criterion.get('index', '') == 'Language':
                language_widget = queryMultiAdapter((widget, self.context),
                                                    ILanguageWidgetAdapter)
                if not language_widget:
                    continue
                query.update(language_widget(kwargs))

        # Add default sorting criteria
        if sort and not query.has_key('sort_on'):
            query['sort_on'] = 'effective'
            query['sort_order'] = 'reverse'

        # Add default language.
        # Also make sure to return language-independent content.
        lang = self.language
        if lang:
            lang = [lang, '']
        query.setdefault('Language', lang)

        logger.debug('QUERY: %s', query)
        return query

    def query(self, batch=True, sort=True, **kwargs):
        """ Search using given criteria
        """
        if self.request:
            kwargs.update(self.request.form)
            kwargs.pop('sort[]', None)
            kwargs.pop('sort', None)

        # jQuery >= 1.4 adds type to params keys
        # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
        # Let's fix this
        kwargs = dict((key.replace('[]', ''), val)
                      for key, val in kwargs.items())

        query = self.criteria(sort=sort, **kwargs)
        catalog = getUtility(IFacetedCatalog)
        try:
            brains = catalog(self.context, **query)
        except Exception, err:
            logger.exception(err)
            return Batch([], 20, 0)
        if not brains:
            return Batch([], 20, 0)

        # Apply after query (filter) on brains
        num_per_page = 20
        criteria = ICriteria(self.context)
        for cid, criterion in criteria.items():
            widgetclass = criteria.widget(cid=cid)
            widget = widgetclass(self.context, self.request, criterion)

            if widget.widget_type == 'resultsperpage':
                num_per_page = widget.results_per_page(kwargs)

            brains_filter = queryAdapter(widget, IWidgetFilterBrains)
            if brains_filter:
                brains = brains_filter(brains, kwargs)

        if not batch:
            return brains

        b_start = safeToInt(kwargs.get('b_start', 0))
        orphans = num_per_page * 20 / 100 # orphans = 20% of items per page

        if type(brains) == GeneratorType:
            brains = [brain for brain in brains]

        return Batch(brains, num_per_page, b_start, orphan=orphans)

    @ramcache(cacheKeyFacetedNavigation, dependencies=['eea.facetednavigation'])
    def __call__(self, *args, **kwargs):
        self.brains = self.query(**kwargs)
        html = self.index()
        return html
