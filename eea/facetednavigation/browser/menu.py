""" Object menus
"""
import logging
from Products.LinguaPlone.browser.menu import TranslateMenu

logger = logging.getLogger('eea.facetednavigation.browser.menu')

class SafeTranslateMenu(TranslateMenu):
    """ LinguaPlone menu does crash when using within portal_fiveactions as
    action provider
    """
    def getMenuItems(self, context, request):
        """ Return menu items for translate menu
        """
        try:
            res = TranslateMenu.getMenuItems(self, context, request)
        except Exception, err:
            logger.debug(err)
            res = []

        return res
