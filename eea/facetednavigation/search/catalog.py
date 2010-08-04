import logging
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from interfaces import IFacetedCatalog
logger = logging.getLogger('eea.facetednavigation.search.catalog')

class FacetedCatalog(object):
    """ Custom faceted adapter for portal_catalog
    """
    implements(IFacetedCatalog)

    def __call__(self, context, **query):
        ctool = getToolByName(context, 'portal_faceted', None)
        if ctool:
            search = ctool.search
        else:
            logger.debug('portal_faceted not present, using portal_catalog')
            ctool = getToolByName(context, 'portal_catalog')
            search = ctool.searchResults

        # Also get query from Topic
        buildQuery = getattr(context, 'buildQuery', None)
        newquery = buildQuery and buildQuery() or {}
        if not isinstance(newquery, dict):
            newquery = {}
        if 'sort_on'in query and 'sort_order' not in query:
            newquery.pop('sort_order', None)
        newquery.update(query)
        return search(**newquery)
