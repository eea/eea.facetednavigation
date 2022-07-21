""" Faceted Views meta directives
"""
from zope.interface import Interface, implementer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.facetednavigation.views.interfaces import IViewsInfo
from Products.Five.browser.metaconfigure import page


@implementer(IViewsInfo)
class ViewsInfo(object):
    """Faceted views registry"""

    _views = {}

    @property
    def views(self):
        """Faceted views"""
        return self._views

    def keys(self):
        """Faceted views names"""
        return list(self.views.keys())

    def label(self, key):
        """Faceted view label or key"""
        return self.views.get(key, key)


def ViewDirective(
    _context,
    name,
    permission,
    for_=Interface,
    layer=IDefaultBrowserLayer,
    template=None,
    class_=None,
    allowed_interface=None,
    allowed_attributes=None,
    attribute="__call__",
    menu=None,
    title=None,
):
    """Faceted view"""
    label = title
    if title and not menu:
        title = None

    page(
        _context=_context,
        name=name,
        permission=permission,
        for_=for_,
        layer=layer,
        template=template,
        class_=class_,
        allowed_interface=allowed_interface,
        allowed_attributes=allowed_attributes,
        attribute=attribute,
        menu=menu,
        title=title,
    )

    ViewsInfo._views[name] = label or name
