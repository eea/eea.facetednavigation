""" Layout upgrades
"""
import logging
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.interfaces import IFacetedNavigable
from zope.component.interface import interfaceToName
logger = logging.getLogger("eea.facetednavigation.upgrades")

def fix_layout(context):
    """ Fix layout for old style IFacetedNavigable objects
    """
    ctool = getToolByName(context, 'portal_catalog')
    iface = interfaceToName(context, IFacetedNavigable)
    brains = ctool(object_provides=iface, show_inactive=True, Language='all')
    for brain in brains:
        doc = brain.getObject()
        layout = doc.getLayout()
        if not layout.startswith('faceted'):
            logger.info("Fixing layout for %s", doc.absolute_url())
            doc.setLayout('facetednavigation_view')
