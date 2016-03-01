""" Upgrade to version 8.8
"""
import logging
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger("eea.facetednavigation")


def install_select2(context):
    """
    In version 8.8, the autocomplete widget uses select2 instead of
    jquery.autocomplete.
    """

    context.runAllImportStepsFromProfile('profile-eea.jquery:23-select2')
    js_tool = getToolByName(context, 'portal_javascripts')
    js_tool.cookResources()
    logger.info('Installed select2 dependency')
