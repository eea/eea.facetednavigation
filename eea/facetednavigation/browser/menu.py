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

        if not IFacetedNavigable.providedBy(context):
            return res

        # Add sync translations menu item
        res.append({
            "title"       : _(u"label_sync_faceted_translations",
                                default=u"Sync faceted translations"),
            "description" : _(u"title_sync_faceted_translations",
                              default=u"Synchronize faceted configuration across translations"),
            "action"      : context.absolute_url() + "/@@faceted_sync_translations",
            "selected"    : False,
            "icon"        : None,
            "extra"       : { "id"        : "_sync_faceted_translations",
                              "separator" : res and "actionSeparator" or None,
                              "class"     : ""
                             },
            "submenu"     : None,
            })

        return res
