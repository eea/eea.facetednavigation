""" Custom catalog
"""
import logging
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from BTrees.IIBTree import IIBucket
from eea.facetednavigation.search.interfaces import IFacetedCatalog
logger = logging.getLogger('eea.facetednavigation.search.catalog')

class FacetedCatalog(object):
    """ Custom faceted adapter for portal_catalog
    """
    implements(IFacetedCatalog)

    def _apply_index(self, index, value):
        """ Default portal_catalog index _apply_index
        """
        index_id = index.getId()

        apply_index = getattr(index, '_apply_index', None)
        if not apply_index:
            return IIBucket(), (index_id,)

        rset = apply_index({index_id: value})
        if not rset:
            return IIBucket(), (index_id,)

        return rset

    def apply_index(self, context, index, value):
        """ Call index _apply_index method of catalog index
        """
        ctool = getToolByName(context, 'portal_faceted', None)
        if ctool:
            return ctool.apply_index(index, value)
        return self._apply_index(index, value)

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
