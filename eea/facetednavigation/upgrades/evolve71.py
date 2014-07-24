""" Upgrade to version 7.1
"""
import logging
from Products.CMFCore.utils import getToolByName
from zope.component.interface import interfaceToName
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedNavigable

logger = logging.getLogger("eea.facetednavigation")

def add_sorting_widget(context):
    """
    As in version 7.1 we removed default sorting by effective date, in order
    to maintain backward compatibility we will add a sorting widget, hidden
    for all faceted navigable items where this widget is not present
    """
    ctool = getToolByName(context, 'portal_catalog')
    iface = interfaceToName(context, IFacetedNavigable)
    brains = ctool.unrestrictedSearchResults(object_provides=iface)

    count = 0
    for brain in brains:
        try:
            doc = brain.getObject()
            settings = ICriteria(doc)
            sorting = [criterion for criterion in settings.values()
                       if criterion.widget == 'sorting']
            if sorting:
                continue

            settings.add(
                'sorting', 'right',
                 title='Sort on', default='effective(reverse)',
                 hidden=True
            )
        except Exception, err:
            logger.exception(err)
        else:
            logger.info('Added sorting widget for: %s', doc.absolute_url())
            count += 1
    logger.info('Added %s sorting widgets', count)
