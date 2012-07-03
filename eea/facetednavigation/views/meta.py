""" Faceted Views meta directives
"""
from zope.interface import Interface, implements
from eea.facetednavigation.views.interfaces import IViewsInfo
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from Products.Five.browser.metaconfigure import page

class ViewsInfo(object):
    """ Faceted views registry
    """
    implements(IViewsInfo)
    _views = {}

    @property
    def views(self):
        """ Faceted views
        """
        return self._views

    def keys(self):
        """ Faceted views names
        """
        return self.views.keys()

    def label(self, key):
        """ Faceted view label or key
        """
        return self.views.get(key, key)

def ViewDirective(_context, name, permission, for_=Interface,
                  layer=IDefaultBrowserLayer, template=None, class_=None,
                  allowed_interface=None, allowed_attributes=None,
                  attribute='__call__', menu=None, title=None):
    """ Faceted view
    """
    label = title
    if title and not menu:
        title = None

    page(_context=_context, name=name, permission=permission,
         for_=for_, layer=layer, template=template, class_=class_,
         allowed_interface=allowed_interface,
         allowed_attributes=allowed_attributes,
         attribute=attribute, menu=menu, title=title)

    ViewsInfo._views[name] = label or name
