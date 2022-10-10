""" Faceted query
"""
from eea.facetednavigation.caching import cacheKeyFacetedNavigation
from eea.facetednavigation.caching import ramcache
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IEEASettings
from eea.facetednavigation.interfaces import IFacetedCatalog
from eea.facetednavigation.interfaces import IFacetedLayout
from eea.facetednavigation.interfaces import IFacetedWrapper
from eea.facetednavigation.interfaces import ILanguageWidgetAdapter
from eea.facetednavigation.interfaces import IWidgetFilterBrains
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.contenttypes.browser.folder import FolderView
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import safeToInt
from types import GeneratorType
from zope.component import getUtility
from zope.component import queryAdapter
from zope.component import queryMultiAdapter

import logging
import time


logger = logging.getLogger("eea.facetednavigation")


class FacetedQueryHandler(FolderView):
    """Faceted Query"""

    def __init__(self, context, request):
        super(FacetedQueryHandler, self).__init__(context, request)
        if request.get("HTTP_X_REQUESTED_WITH", "") == "XMLHttpRequest":
            registry = getUtility(IRegistry)
            settings = registry.forInterface(IEEASettings, check=False)
            if settings.disable_diazo_rules_ajax:
                request.response.setHeader("X-Theme-Disabled", "1")

    def macros(self, name="content-core"):
        """Return macro from default layout"""
        return IFacetedLayout(self.context).get_macro(macro=name)

    @property
    def language(self):
        """Get context language"""
        lang = getattr(self.context, "getLanguage", None)
        if lang:
            return lang()
        return self.request.get("LANGUAGE", "")

    @property
    def default_criteria(self):
        """Return default criteria"""
        query = {}
        criteria = queryAdapter(self.context, ICriteria)
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)
            widget = widget(self.context, self.request, criterion)
            default = widget.default
            if not default:
                continue
            query[cid] = default
        return query

    def get_context(self, content=None):
        """Return context"""
        wrapper = queryAdapter(self.context, IFacetedWrapper)
        if not wrapper:
            return self.context
        return wrapper(content)

    def criteria(self, sort=False, **kwargs):
        """Process catalog query"""
        if self.request:
            kwargs.update(self.request.form)

        # jQuery >= 1.4 adds type to params keys
        # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
        # Let's fix this
        kwargs = dict((key.replace("[]", ""), val) for key, val in kwargs.items())

        logger.debug("REQUEST: %r", kwargs)

        # Generate the catalog query
        criteria = ICriteria(self.context)
        query = {}
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)
            widget = widget(self.context, self.request, criterion)

            widget_query = widget.query(kwargs)
            if getattr(widget, "faceted_field", False):
                widget_index = widget.data.get("index", "")
                if "facet.field" in query and widget_index not in query["facet.field"]:
                    query["facet.field"].append(widget_index)
                else:
                    query["facet.field"] = [widget_index]
            query.update(widget_query)

            # Handle language widgets
            if criterion.get("index", "") == "Language":
                language_widget = queryMultiAdapter(
                    (widget, self.context), ILanguageWidgetAdapter
                )
                if not language_widget:
                    continue
                query.update(language_widget(kwargs))

        # Add default sorting criteria
        if sort and "sort_on" not in query:
            query["sort_on"] = "effective"
            query["sort_order"] = "reverse"

        # Add default language.
        # Also make sure to return language-independent content.
        lang = self.language
        if lang:
            lang = [lang, ""]
        query.setdefault("Language", lang)

        logger.debug("QUERY: %s", query)
        return query

    def query(self, batch=True, sort=False, **kwargs):
        """Search using given criteria"""
        if self.request:
            kwargs.update(self.request.form)
            kwargs.pop("sort[]", None)
            kwargs.pop("sort", None)

        # jQuery >= 1.4 adds type to params keys
        # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
        # Let's fix this
        kwargs = dict((key.replace("[]", ""), val) for key, val in kwargs.items())

        query = self.criteria(sort=sort, **kwargs)
        # We don't want to do an unnecessary sort for a counter query
        counter_query = kwargs.pop("counter_query", False)
        if counter_query:
            query.pop("sort_on", None)
            query.pop("sort_order", None)

        catalog = getUtility(IFacetedCatalog)
        num_per_page = 20
        criteria = ICriteria(self.context)
        brains_filters = []
        for cid, criterion in criteria.items():
            widgetclass = criteria.widget(cid=cid)
            widget = widgetclass(self.context, self.request, criterion)

            if widget.widget_type == "resultsperpage":
                num_per_page = widget.results_per_page(kwargs)

            brains_filter = queryAdapter(widget, IWidgetFilterBrains)
            if brains_filter:
                brains_filters.append(brains_filter)

        b_start = safeToInt(kwargs.get("b_start", 0))
        # make sure orphans is an integer, // is used so in Python3 we have an
        # integer division as by default, a division result is a float
        orphans = num_per_page * 20 // 100  # orphans = 20% of items per page
        if batch and not brains_filters:
            # add b_start and b_size to query to use better sort algorithm
            query["b_start"] = b_start
            query["b_size"] = num_per_page + orphans

        try:
            brains = catalog(self.context, **query)
        except Exception as err:
            logger.exception(err)
            return Batch([], 20, 0)
        if not brains:
            return Batch([], 20, 0)

        # Apply after query (filter) on brains
        start = time.time()
        for brains_filter in brains_filters:
            brains = brains_filter(brains, kwargs)

        if not batch:
            return brains

        if isinstance(brains, GeneratorType):
            brains = [brain for brain in brains]

        delta = time.time() - start
        if delta > 30:
            logger.warn(
                "Very slow IWidgetFilterBrains adapters: %s at %s",
                brains_filters,
                self.context.absolute_url(),
            )
        return Batch(brains, num_per_page, b_start, orphan=orphans)

    def results(self, **kwargs):
        """Faceted results"""
        kwargs["batch"] = False
        results = self.query(**kwargs)
        if isinstance(results, GeneratorType):
            results = [i for i in results]
        results = IContentListing(results)
        return results

    @ramcache(cacheKeyFacetedNavigation, dependencies=["eea.facetednavigation"])
    def __call__(self, *args, **kwargs):
        self.brains = self.query(**kwargs)
        html = self.index()
        return html
