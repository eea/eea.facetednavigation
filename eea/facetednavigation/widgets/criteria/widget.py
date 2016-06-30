""" Criteria widget
"""
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.criteria.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.criteria.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'criteria'
    widget_label = _('Filters')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')
