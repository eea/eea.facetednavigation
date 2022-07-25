""" Select widget
"""
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.select.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.select.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.select.interfaces import CountableSchemata
from eea.facetednavigation.widgets.select.interfaces import DisplaySchemata
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _

import six


class Widget(CountableWidget):
    """ Widget
    """
    widget_type = 'select'
    widget_label = _('Select')

    groups = (
        DefaultSchemata,
        LayoutSchemata,
        CountableSchemata,
        DisplaySchemata
    )

    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Get default values
        """
        default = super(Widget, self).default or u''
        if six.PY2:
            if isinstance(default, six.text_type):
                default = default.encode('utf-8')
        return default

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        if six.PY2:
            index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        if not value:
            return query

        query[index] = value
        return query
