""" Menu
"""
from zope import interface
import logging
from zope.component import queryAdapter
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.publisher.browser.menu import BrowserMenu
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView

from eea.facetednavigation.layout.interfaces import ILayoutMenuHandler
from eea.facetednavigation.layout.interfaces import IFacetedLayout

logger = logging.getLogger('eea.facetednavigation.layout.menu')

class LayoutMenu(BrowserMenu):
    """ Layout menu
    """
    interface.implements(IBrowserMenu)

    def _get_menuitems(self, context):
        """ Menu items
        """
        res = []
        faceted_adapter = queryAdapter(context, IFacetedLayout)
        if not faceted_adapter:
            return res

        for layout, title in faceted_adapter.layouts:
            res.append({
            'title': title,
            'description': title,
            'action': '@@faceted_layout?layout=%s' % layout,
            'selected': layout == faceted_adapter.layout,
            'extra': {'id': layout,
                      'separator': None},
            'icon': u'',
            'submenu': None,
            'subtype': u''
            })
        return res

    def getMenuItems(self, obj, request):
        """ Safely get menu items
        """
        try:
            return self._get_menuitems(obj)
        except Exception, err:
            logger.exception(err)
            raise

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
