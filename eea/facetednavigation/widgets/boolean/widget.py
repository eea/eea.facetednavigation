""" Checkbox widget
"""
from plone.i18n.normalizer import urlnormalizer as normalizer
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
    def css_class(self):
        """ Widget specific css class
        """
        css_type = self.widget_type
        css_title = normalizer.normalize(self.data.title)
        return ('faceted-checkboxes-widget '
                'faceted-{0}-widget section-{1}').format(css_type, css_title)

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
