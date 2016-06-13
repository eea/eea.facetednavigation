""" Faceted widgets
"""
from zope import interface
from zope.component.zcml import adapter
from eea.facetednavigation.widgets.interfaces import ICriterion
from eea.facetednavigation.widgets.interfaces import IWidgetsInfo


class WidgetsInfo(object):
    """ Widgets registry
    """
    interface.implements(IWidgetsInfo)
    _widgets = {}

    @property
    def widgets(self):
        """ Widgets
        """
        return self._widgets

    def __call__(self, key):
        """ Get widget by key or raise
        """
        return self._widgets.get(key)

class WidgetData(object):
    """ Get data to populate widget with
    """
    def __init__(self, context):
        self.context = context

    def __getattr__(self, name, default=None):
        return getattr(self.context, name, default)

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
        # raise TypeError(
        #     "No schema provided for faceted widget type '%s'" % name)
        import logging
        logger = logging.getLogger("eea.facetednavigation")
        logger.warn("No schema provided for faceted widget type '%s'" % name)
    else:
        adapter(
            _context=_context,
            provides=schema,
            factory=(accessor,),
            for_=(criterion,)
        )
