""" Checkbox widget
"""
from Products.CMFCore.utils import getToolByName

from eea.facetednavigation import EEAMessageFactory as _
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
        return default.encode('utf-8')

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

        catalog = getToolByName(self.context, 'portal_catalog')
        if index in catalog.Indexes:
            if catalog.Indexes[index].meta_type == 'BooleanIndex':
                if value == 'False':
                    value = False
                elif value == 'True':
                    value = True

        query[index] = value
        return query
