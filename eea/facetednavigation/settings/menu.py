""" Faceted settings
"""
from zope.interface import implements, alsoProvides, noLongerProvides
from zope.security import checkPermission
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from eea.facetednavigation.settings import BrowserMenu
from eea.facetednavigation.settings import BrowserSubMenuItem
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.settings.interfaces import ISettingsHandler
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn
from eea.facetednavigation.settings.interfaces import IDisableSmartFacets
from eea.facetednavigation.settings.interfaces import IDontInheritConfiguration
from eea.facetednavigation import EEAMessageFactory as _

class SettingsMenu(BrowserSubMenuItem):
    """ Faceted settings menu
    """
    title = _(u'Faceted settings')
    description = _(u'Faceted global settings')

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
        # use format to avoid messing with url with "%" in them like
        # 'http://foo/stones-1/foo%20bar%20moo/@@faceted_settings/%s'
        action = url + '/@@faceted_settings/{0}'

        left_hidden = IHidePloneLeftColumn.providedBy(context)
        right_hidden = IHidePloneRightColumn.providedBy(context)
        smart_hidden = IDisableSmartFacets.providedBy(context)

        menu = [
            {
                'title': (_('Enable left portlets') if left_hidden
                     else _('Disable left portlets')),
                'description': '',
                'action': action.format('toggle_left_column'),
                'selected': not left_hidden,
                'icon': ('++resource++faceted_images/show.png' if left_hidden
                    else '++resource++faceted_images/hide.png'),
                'extra': {
                    'id': 'toggle_left_column',
                    'separator': None,
                    'class': ''
                    },
                'submenu': None,
            },
            {
                'title': (_('Enable right portlets') if right_hidden
                     else _('Disable right portlets')),
                'description': '',
                'action': action.format('toggle_right_column'),
                'selected': not right_hidden,
                'icon': ('++resource++faceted_images/show.png' if right_hidden
                    else '++resource++faceted_images/hide.png'),
                'extra': {
                    'id': 'toggle_right_column',
                    'separator': None,
                    'class': ''
                    },
                'submenu': None,
            },
            {
                'title': (_('Enable smart facets hiding') if smart_hidden
                     else _('Disable smart facets hiding')),
                'description': '',
                'action': action.format('toggle_smart_facets'),
                'selected': not smart_hidden,
                'icon': ('++resource++faceted_images/show.png' if smart_hidden
                    else '++resource++faceted_images/hide.png'),
                'extra': {
                    'id': 'disable_smart_facets',
                    'separator': None,
                    'class': ''
                    },
                'submenu': None,
            },
        ]
        iscanonical = getattr(context, 'isCanonical', None)
        if callable(iscanonical) and not iscanonical():
            inherit_config = not IDontInheritConfiguration.providedBy(context)
            menu.append({
                'title': (_('Disable inheriting configuration')
                          if inherit_config
                          else _('Enable inheriting configuration ')),
                'description': '',
                'action': action.format('toggle_inherit_config'),
                'selected': not inherit_config,
                'icon': None,
                'extra': {
                    'id': 'toggle_inherit_config',
                    'separator': None,
                    'class': ''
                    },
                'submenu': None,
            })

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
    def toggle_left_column(self, **kwargs):
        """ Show / hide plone portlets left column
        """
        if IHidePloneLeftColumn.providedBy(self.context):
            noLongerProvides(self.context, IHidePloneLeftColumn)
            return self._redirect(_('Portlets left column is visible now'))
        else:
            alsoProvides(self.context, IHidePloneLeftColumn)
            return self._redirect(_('Portlets left column is hidden now'))

    def toggle_right_column(self, **kwargs):
        """ Show / hide plone portlets left column
        """
        if IHidePloneRightColumn.providedBy(self.context):
            noLongerProvides(self.context, IHidePloneRightColumn)
            return self._redirect(_('Portlets right column is visible now'))
        else:
            alsoProvides(self.context, IHidePloneRightColumn)
            return self._redirect(_('Portlets right column is hidden now'))

    def toggle_smart_facets(self, **kwargs):
        """ Enable/Disable 'smart facets hiding'
        """
        if IDisableSmartFacets.providedBy(self.context):
            noLongerProvides(self.context, IDisableSmartFacets)
            return self._redirect(_('Smart facets hiding is now enabled'))
        else:
            alsoProvides(self.context, IDisableSmartFacets)
            return self._redirect(_('Smart facets hiding is now disabled'))

    def toggle_inherit_config(self, **kwargs):
        """ Enable/Disable 'inheriting configuration'
        """
        if IDontInheritConfiguration.providedBy(self.context):
            noLongerProvides(self.context, IDontInheritConfiguration)
            return self._redirect(
                _('Inheriting configuration if is now enabled'))
        else:
            alsoProvides(self.context, IDontInheritConfiguration)
            return self._redirect(
                _('Inheriting configuration is now disabled'))
