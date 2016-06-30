""" ETag widget
"""
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.etag.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.etag.interfaces import LayoutSchemata

class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'etag'
    widget_label = 'ETag'

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')
