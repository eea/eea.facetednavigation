""" Faceted sub-menu
"""
from zope import interface
from zope.component import queryAdapter
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from plone.app.contentmenu.interfaces import IActionsSubMenuItem

class LayoutSubMenuItem(BrowserSubMenuItem):
    """ Layout
    """
    interface.implements(IActionsSubMenuItem)

    title = u'Layout'
    description = u''
    submenuId = u'layout'
    order = 9
    extra = {'id': 'layout'}

    @property
    def action(self):
        """ Sub-menu action
        """
        return self.context.absolute_url()+ '/@@faceted_layout'

    def available(self):
        """ Available layouts
        """
        layout_adapter = queryAdapter(self.context, IFacetedLayout)
        if not layout_adapter:
            return False
        return not not layout_adapter.layouts
