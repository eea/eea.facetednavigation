""" Upgrade to version 8.8
"""
import logging
from zope.component import queryAdapter
from zope.component.interface import interfaceToName
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.interfaces import ICriteria, IFacetedNavigable

logger = logging.getLogger("eea.facetednavigation")


def fix_criteria(context):
    """
    In version 8.8, the autocomplete widget uses select2 instead of
    jquery.autocomplete.
    """
    ctool = getToolByName(context, 'portal_catalog')
    iface = interfaceToName(context, IFacetedNavigable)
    brains = ctool.unrestrictedSearchResults(object_provides=iface)

    logger.info('Fixing %s faceted navigable criteria', len(brains))
    for brain in brains:
        doc = brain.getObject()
        criteria = queryAdapter(doc, ICriteria)
        for cid, criterion in criteria.items():
            logger.info('Fixing faceted criteria for %s', brain.getURL())
            properties = criterion.__dict__
            criteria.edit(cid, **properties)
    logger.info('Done fixing faceted navigable criteria')
