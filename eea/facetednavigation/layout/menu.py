""" Menu
"""
from zope import interface
import logging
from zope.component import queryAdapter
from plone.app.contentmenu.menu import DisplayMenu
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView

from eea.facetednavigation.layout.interfaces import ILayoutMenuHandler
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable

logger = logging.getLogger('eea.facetednavigation.layout.menu')

class FacetedDisplayMenu(DisplayMenu):
    """ Overrides display menu
    """
    def getMenuItems(self, obj, request):
        """ Safely get menu items
        """
        res = super(FacetedDisplayMenu, self).getMenuItems(obj, request)
        if not IFacetedNavigable.providedBy(obj):
            return res

        faceted_adapter = queryAdapter(obj, IFacetedLayout)
        if not faceted_adapter:
            return []

        new = []
        allowed = set(x[0] for x in faceted_adapter.layouts)
        current = faceted_adapter.layout
        for item in res:
            layout = item.get(
                'extra', {}).get('id', '').replace('folder-', '', 1)

            if  not layout in allowed:
                continue

            item['action'] = '@@faceted_layout?layout=%s' % layout
            if (layout == current):
                item['selected'] = True
                item['extra']['class'] = 'actionMenuSelected'
            new.append(item)
        return new

class LayoutMenuHandler(BrowserView):
    """ Layout support
    """
    interface.implements(ILayoutMenuHandler)

    def _redirect(self, msg):
        """ Set status message to msg and redirect to context absolute_url
        """
        url = self.context.absolute_url()
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        self.request.response.redirect(url)
        return ''

    def __call__(self):
        layout = self.request.get('layout', None)
        err = IFacetedLayout(self.context).update_layout(layout)
        if not err:
            return self._redirect('Layout changed')
        return self._redirect(err)
