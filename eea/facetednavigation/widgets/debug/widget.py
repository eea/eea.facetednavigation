""" Widget
"""
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.debug.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.debug.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'debug'
    widget_label = _('Debugger')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')
