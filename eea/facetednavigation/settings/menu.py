""" Faceted settings
"""
from zope.interface import implements, alsoProvides, noLongerProvides
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from zope.app.publisher.browser.menu import BrowserMenu
from zope.security import checkPermission

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.settings.interfaces import ISettingsHandler
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn
from eea.facetednavigation import EEAMessageFactory as _

class SettingsMenu(BrowserSubMenuItem):
    """ Faceted settings menu
    """
    title = _(u'label_faceted_settings_menu',
              default=u'Faceted settings')
    description = _(u'help_faceted_settings_menu',
                    default=u'Faceted global settings')

    submenuId = 'faceted_settings_actions'
    order = 5
    extra = {'id': 'faceted_settings'}

    @property
    def action(self):
        """ Submenu action
        """
        return self.context.absolute_url()

    def available(self):
        """ Is this menu available?
        """
        return (IFacetedNavigable.providedBy(self.context) and
                checkPermission('eea.faceted.configure', self.context))

    def selected(self):
        """ Is this item selected?
        """
        return False

class SettingsMenuItems(BrowserMenu):
    """ Faceted global settings menu items
    """
    def getMenuItems(self, context, request):
        """ Return menu items
        """
        url = context.absolute_url()
        action = url + '/@@faceted_settings/%s'

        left_hidden = IHidePloneLeftColumn.providedBy(context)
        right_hidden = IHidePloneRightColumn.providedBy(context)

        menu = [
            {
                'title': (_('Enable left portlets') if left_hidden
                     else _('Disable left portlets')),
                'description': '',
                'action': action % 'hide_left_column',
                'selected': not left_hidden,
                'icon': ('++resource++faceted_images/show.png' if left_hidden
                    else '++resource++faceted_images/hide.png'),
                'extra': {
                    'id': 'hide_left_column',
                    'separator': None,
                    'class': ''
                    },
                'submenu': None,
            },
            {
                'title': (_('Enable right portlets') if right_hidden
                     else _('Disable right portlets')),
                'description': '',
                'action': action % 'hide_right_column',
                'selected': not right_hidden,
                'icon': ('++resource++faceted_images/show.png' if right_hidden
                    else '++resource++faceted_images/hide.png'),
                'extra': {
                    'id': 'hide_right_column',
                    'separator': None,
                    'class': ''
                    },
                'submenu': None,
            },
        ]

        return menu

class SettingsHandler(BrowserView):
    """ Edit faceted global settings
    """
    implements(ISettingsHandler)

    def _redirect(self, msg=''):
        """ Redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(msg, type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg
    #
    # Public interface
    #
    def hide_left_column(self, **kwargs):
        """ Hide plone portlets left column
        """
        if IHidePloneLeftColumn.providedBy(self.context):
            noLongerProvides(self.context, IHidePloneLeftColumn)
            return self._redirect(_('Portlets left column is visible now'))
        else:
            alsoProvides(self.context, IHidePloneLeftColumn)
            return self._redirect(_('Portlets left column is hidden now'))

    def hide_right_column(self, **kwargs):
        """ Hide plone portlets left column
        """
        if IHidePloneRightColumn.providedBy(self.context):
            noLongerProvides(self.context, IHidePloneRightColumn)
            return self._redirect(_('Portlets right column is visible now'))
        else:
            alsoProvides(self.context, IHidePloneRightColumn)
            return self._redirect(_('Portlets right column is hidden now'))
