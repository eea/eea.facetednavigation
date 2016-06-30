""" Checkbox widget
"""
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.boolean.interfaces import (
    DefaultSchemata,
    LayoutSchemata,
    CountableSchemata
)

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'boolean'
    widget_label = _('Boolean')
    groups = (DefaultSchemata, LayoutSchemata, CountableSchemata)

    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Get default values
        """
        return bool(self.data.get('default', None))

    def selected(self):
        """ Return True if True by default
        """
        return self.default or False

    def vocabulary(self):
        """ Vocabulary
        """
        return [(1, 1)]

    def index_id(self):
        """ Index
        """
        return self.data.get('index', '').lower()

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')

        if not index:
            return {}

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        if value:
            return {index: True}
        else:
            return {}
