import logging
from Products.LinguaPlone.browser.menu import TranslateMenu
from Products.LinguaPlone import LinguaPloneMessageFactory as _
from eea.facetednavigation.interfaces import IFacetedNavigable

logger = logging.getLogger('eea.facetednavigation.browser.menu')

class SafeTranslateMenu(TranslateMenu):
    """ LinguaPlone menu does crash when using within portal_fiveactions as
    action provider
    """
    def getMenuItems(self, context, request):
        try:
            res = TranslateMenu.getMenuItems(self, context, request)
        except Exception, err:
            logger.debug(err)
            res = []

        return res
