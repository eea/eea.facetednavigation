""" Checkbox widget
"""
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.dexterity_support import normalize as atdx_normalize
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.radio.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.radio.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.radio.interfaces import CountableSchemata
from eea.facetednavigation.widgets.radio.interfaces import DisplaySchemata
from eea.facetednavigation.widgets.widget import CountableWidget


class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'radio'
    widget_label = _('Radio')
    view_js = '++resource++eea.facetednavigation.widgets.radio.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.radio.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.radio.view.css'

    groups = (
        DefaultSchemata,
        LayoutSchemata,
        CountableSchemata,
        DisplaySchemata
    )

    index = ViewPageTemplateFile('widget.pt')

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')
        if not value:
            return query

        value = atdx_normalize(value)

        query[index] = value
        return query
