""" Menu
"""
import logging
from zope.interface import implementer
from zope.component import queryAdapter
from plone.app.contentmenu.menu import DisplayMenu
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from eea.facetednavigation.plonex import addTokenToUrl
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
            return res

        new = []
        template = {
            'submenu': None,
            'description': '',
            'extra': {
                'separator': None,
                'id': '',
                'class': ''},
            'selected': False,
            'action': '',
            'title': '',
            'icon': None
        }

        current = faceted_adapter.layout
        for name, label in faceted_adapter.layouts:
            layout = template.copy()
            layout['extra'] = template['extra'].copy()
            layout['extra']['id'] = name
            layout['title'] = label
            url = '%s/@@faceted_layout?layout=%s' % (obj.absolute_url(), name)
            layout['action'] = addTokenToUrl(url, request)

            if name == current:
                layout['selected'] = True
                layout['extra']['class'] = 'actionMenuSelected'

            new.append(layout)

        return new


@implementer(ILayoutMenuHandler)
class LayoutMenuHandler(BrowserView):
    """ Layout support
    """
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
