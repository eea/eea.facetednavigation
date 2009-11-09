from zope import interface
from interfaces import IWidgetsInfo

class WidgetsInfo(object):
    """
    """
    interface.implements(IWidgetsInfo)
    _widgets = {}

    @property
    def widgets(self):
        """
        """
        return self._widgets

    def __call__(self, key):
        """ Get widget by key or raise
        """
        return self._widgets.get(key)

def WidgetDirective(_context, factory=None, **kwargs):
    """ Register faceted widgets
    """
    if not factory:
        raise TypeError("No factory provided")

    name = getattr(factory, 'widget_type', None)
    if not name:
        raise TypeError("Invalid factory: widget_type property is empty or not defined")

    WidgetsInfo._widgets[name] = factory
