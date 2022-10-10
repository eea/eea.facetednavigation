""" Custom catalog
"""
from BTrees.IIBTree import IIBucket
from eea.facetednavigation.events import QueryWillBeExecutedEvent
from eea.facetednavigation.search.interfaces import IFacetedCatalog
from plone.app.contenttypes.behaviors.collection import (
    ICollection as ICollectionBehavior,
)
from plone.app.contenttypes.interfaces import ICollection
from plone.app.querystring.queryparser import parseFormquery
from Products.CMFCore.utils import getToolByName
from zope.event import notify
from zope.interface import implementer

import logging


logger = logging.getLogger("eea.facetednavigation")


@implementer(IFacetedCatalog)
class FacetedCatalog(object):
    """Custom faceted adapter for portal_catalog"""

    def _apply_index(self, index, value):
        """Default portal_catalog index _apply_index"""
        index_id = index.getId()

        apply_index = getattr(index, "_apply_index", None)
        if not apply_index:
            return IIBucket(), (index_id,)

        rset = apply_index({index_id: value})

        if not rset:
            return IIBucket(), (index_id,)

        return rset

    def apply_index(self, context, index, value):
        """Call index _apply_index method of catalog index"""
        ctool = getToolByName(context, "portal_faceted", None)
        if ctool:
            return ctool.apply_index(index, value)
        return self._apply_index(index, value)

    def __call__(self, context, **query):
        ctool = getToolByName(context, "portal_faceted", None)
        if ctool:
            search = ctool.search
        else:
            logger.debug("portal_faceted not present, using portal_catalog")
            ctool = getToolByName(context, "portal_catalog")
            search = ctool.searchResults

        # Also get query from Topic
        buildQuery = getattr(context, "buildQuery", None)
        newquery = buildQuery and buildQuery() or {}
        formquery = None

        # Get query from Collection
        if ICollection.providedBy(context):
            infos = ICollectionBehavior(context)
            sort_order = "descending" if infos.sort_reversed else "ascending"
            sort_on = infos.sort_on
            formquery = infos.query

        if formquery is not None:
            newquery = parseFormquery(context, formquery, sort_on, sort_order)

        if not isinstance(newquery, dict):
            newquery = {}

        # Avoid mixing sorting params from faceted and collection
        if "sort_on" not in query:
            query.pop("sort_order", None)

        if "sort_on" in query and "sort_order" not in query:
            newquery.pop("sort_order", None)

        newquery.update(query)

        notify(QueryWillBeExecutedEvent(context, newquery))
        return search(**newquery)
