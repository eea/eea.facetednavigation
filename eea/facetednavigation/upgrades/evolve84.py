""" Upgrade to version 8.4
"""
import logging
from Products.CMFCore.utils import getToolByName
from zope.component.interface import interfaceToName
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedNavigable

logger = logging.getLogger("eea.facetednavigation")


def migrate_autocomplete_widget(context):
    """
    As in version 8.4 we added selection of the autocomplete suggestion
    view. To maintain backward compatibility we will set the value of
    this 'autocomplete_view' field to solr suggestions view.
    """
    ctool = getToolByName(context, 'portal_catalog')
    iface = interfaceToName(context, IFacetedNavigable)
    brains = ctool.unrestrictedSearchResults(object_provides=iface)

    count = 0
    for brain in brains:
        doc = brain.getObject()
        settings = ICriteria(doc)

        for criterion in settings.values():
            if criterion.widget == 'autocomplete':
                criterion.autocomplete_view = u'solr-autocomplete-suggest'
                logger.info(
                    'Set defaut autocomplete view of widget: %s',
                    criterion.title
                )
                count += 1

    logger.info('Migrated %s autocomplete widgets', count)
