""" Checkbox widget
"""
from plone.i18n.normalizer import urlnormalizer as normalizer
from Products.CMFCore.utils import getToolByName

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.faceted.vocabularies.utils import compare
from eea.facetednavigation.widgets.checkbox.interfaces import (
    DefaultSchemata,
    LayoutSchemata,
    CountableSchemata,
    DisplaySchemata,
)
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _


class Widget(CountableWidget):
    """ Widget
    """
    widget_type = 'checkbox'
    widget_label = _('Checkboxes')

    groups = (
        DefaultSchemata,
        LayoutSchemata,
        CountableSchemata,
        DisplaySchemata
    )

    index = ViewPageTemplateFile('widget.pt')

    @property
    def css_class(self):
        """ Widget specific css class
        """
        css_type = self.widget_type
        css_title = normalizer.normalize(self.data.title)
        return ('faceted-checkboxes-widget '
                'faceted-{0}-widget section-{1}').format(css_type, css_title)


    @property
    def default(self):
        """ Get default values
        """
        default = super(Widget, self).default
        if not default:
            return []

        if isinstance(default, (str, unicode)):
            default = [default, ]
        return [x.encode('utf-8') for x in default]

    def selected(self, key):
        """ Return True if key in self.default
        """
        default = self.default
        if not default:
            return False
        for item in default:
            if compare(key, item) == 0:
                return True
        return False

    @property
    def operator_visible(self):
        """ Is operator visible for anonymous users
        """
        return self.data.get('operator_visible', False)

    @property
    def operator(self):
        """ Get the default query operator
        """
        return self.data.get('operator', 'and')

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')

        if not self.operator_visible:
            operator = self.operator
        else:
            operator = form.get(self.data.getId() + '-operator', self.operator)

        operator = operator.encode('utf-8', 'replace')

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

        query[index] = {'query': value, 'operator': operator}
        return query
