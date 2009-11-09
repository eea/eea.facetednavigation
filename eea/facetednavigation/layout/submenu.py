from zope import interface
from zope.component import queryAdapter
from interfaces import IFacetedLayout
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from plone.app.contentmenu.interfaces import IActionsSubMenuItem

class LayoutSubMenuItem(BrowserSubMenuItem):
    interface.implements(IActionsSubMenuItem)

    title = u'Layout'
    description = u''
    submenuId = u'layout'
    order = 9
    extra = {'id': 'layout'}

    @property
    def action(self):
        return self.context.absolute_url()+ '/@@faceted_layout'

    def available(self):
        layout_adapter = queryAdapter(self.context, IFacetedLayout)
        if not layout_adapter:
            return False
        return not not layout_adapter.layouts
