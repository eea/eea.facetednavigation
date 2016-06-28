""" Faceted widgets
"""
from zope.interface import implementer
from zope.component.zcml import adapter
from eea.facetednavigation.widgets.interfaces import ICriterion
from eea.facetednavigation.widgets.interfaces import IWidgetsInfo


@implementer(IWidgetsInfo)
class WidgetsInfo(object):
    """ Widgets registry
    """
    _widgets = {}
    _schemas = {}

    @property
    def widgets(self):
        """ Widgets
        """
        return self._widgets

    @property
    def schemas(self):
        """ Widgets schemas
        """
        return self._schemas

    def widget(self, name, default=None):
        """ Get widget by name
        """
        return self.widgets.get(name, default)

    def schema(self, name, default=None):
        """ Return widget schema by name
        """
        return self.schemas.get(name, default)

    def __call__(self, key):
        """ Get widget by key or raise
        """
        return self.widgets.get(key)


class WidgetData(object):
    """ Get data to populate widget with
    """
    def __init__(self, context):
        self.context = context

    def __getattr__(self, name, default=None):
        return self.context.get(name, default)

def WidgetDirective(_context, factory=None, schema=None,
                    accessor=WidgetData, criterion=ICriterion, **kwargs):
    """ Register faceted widgets
    """
    if not factory:
        raise TypeError("No factory provided")

    name = getattr(factory, 'widget_type', None)
    if not name:
        raise TypeError(
            "Invalid factory: widget_type property is empty or not defined")

    WidgetsInfo._widgets[name] = factory

    if schema is None:
        raise TypeError(
            "No schema provided for faceted widget type '%s'" % name)

    WidgetsInfo._schemas[name] = schema
    adapter(
        _context=_context,
        provides=schema,
        factory=(accessor,),
        for_=(criterion,)
    )
