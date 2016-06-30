""" Faceted widgets
"""
import warnings
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

    #
    # Ensure custom Faceted Navigation widgets were upgraded
    #
    edit_schema = getattr(factory, 'edit_schema', None)
    if edit_schema is not None:
        warnings.warn(
            "'edit_schema' attribute is deprecated. "
            "Please remove it from your custom Faceted Widget: %s" % name,
            DeprecationWarning)

    view_schema = getattr(factory, 'view_schema', None)
    if view_schema is not None:
        warnings.warn(
            "'view_schema' attribute is deprecated. "
            "Please remove it from your custom Faceted Widget: %s" % name,
            DeprecationWarning)

    view_css = getattr(factory, 'view_css', None)
    if view_css is not None:
        warnings.warn(
            "'view_css' attribute is deprecated. "
            "Please remove it from your custom Faceted Widget: %s "
            "and register it within registry.xml/cssregistry,xml" % name,
            DeprecationWarning)

    edit_css = getattr(factory, 'edit_css', None)
    if edit_css is not None:
        warnings.warn(
            "'edit_css' attribute is deprecated. "
            "Please remove it from your custom Faceted Widget: %s "
            "and register it within registry.xml/cssregistry,xml" % name,
            DeprecationWarning)

    view_js = getattr(factory, 'view_js', None)
    if view_js is not None:
        warnings.warn(
            "'view_js' attribute is deprecated. "
            "Please remove it from your custom Faceted Widget: %s "
            "and register it within registry.xml/jsregistry,xml" % name,
            DeprecationWarning)

    edit_js = getattr(factory, 'edit_js', None)
    if edit_js is not None:
        warnings.warn(
            "'edit_js' attribute is deprecated. "
            "Please remove it from your custom Faceted Widget: %s "
            "and register it within registry.xml/jsregistry,xml" % name,
            DeprecationWarning)
