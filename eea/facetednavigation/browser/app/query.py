import logging
from zope.component import queryMultiAdapter
from zope.component import getUtility
from zope.component import queryAdapter

from Products.CMFCore.utils import getToolByName
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

    def macros(self, name='listing'):
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
        logger.debug(kwargs)

        # Generate the catalog query
        mtool = getToolByName(self.context, 'portal_membership', None)
        criteria = ICriteria(self.context)

        query = {}
        if mtool.isAnonymousUser():
            query['review_state'] = 'published'

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

        # Add default language
        query.setdefault('Language', self.language)

        logger.debug(query)
        return query

    def query(self, batch=True, sort=True, **kwargs):
        """ Search using given criteria
        """
        if self.request:
            kwargs.update(self.request.form)

        query = self.criteria(sort=sort, **kwargs)
        catalog = getUtility(IFacetedCatalog)
        try:
            brains = catalog(self.context, **query)
        except Exception, err:
            logger.exception(err)
            return Batch([], 20, 0)

        # Apply after query on brains
        num_per_page = 20
        criteria = ICriteria(self.context)
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)
            widget = widget(self.context, self.request, criterion)

            if widget.widget_type == 'resultsperpage':
                num_per_page = widget.results_per_page(kwargs)

            aquery = queryAdapter(widget, IWidgetFilterBrains)
            if aquery:
                brains = aquery(brains, kwargs)

        # Render results
        b_start = int(kwargs.get('b_start', 0))
        # orphans = 20% of items per page
        orphans = num_per_page * 20 / 100

        brains = brains and [brain for brain in brains] or []
        if batch:
            return Batch(brains, num_per_page, b_start, orphan=orphans)
        return brains

    @ramcache(cacheKeyFacetedNavigation, dependencies=['eea.facetednavigation'])
    def __call__(self, *args, **kwargs):
        return self.index(query=kwargs)
