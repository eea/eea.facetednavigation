""" Text widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _
from Products.Archetypes.Field import BooleanField
from Products.Archetypes.Widget import BooleanWidget


EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.TextCatalogIndexes',
        widget=SelectionWidget(
            label=_(u'Catalog index'),
            description=_(u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_(u'Default value'),
            description=_(u'Default string to search for'),
            i18n_domain="eea"
        )
    ),
    BooleanField('onlyallelements',
        schemata="default",
        widget=BooleanWidget(
            label=_(u'Search in all elements only'),
            description=_(u'If this checkbox is checked, hides the choice to '
                          'filter in all items or in current items only'),
            i18n_domain="eea"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'text'
    widget_label = _('Text field')
    view_js = '++resource++eea.facetednavigation.widgets.text.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.text.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.text.view.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema

    def quotestring(self, string):
        """ Quote given string
        """
        return '"%s"' % string

    def quote_bad_chars(self, string):
        """ Quote bad chars in query string
        """
        bad_chars = ["(", ")"]
        for char in bad_chars:
            string = string.replace(char, self.quotestring(char))
        return string

    def normalize_string(self, value):
        """ Process string values to be used in catalog query
        """
        # Ensure words are string instances as ZCatalog requires strings
        if isinstance(value, str):
            value = value.decode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        value = self.quote_bad_chars(value)
        return value

    def normalize_list(self, value):
        """ Process list values to be used in catalog query
        """
        return [self.normalize_string(word) for word in value]

    def normalize(self, value):
        """ Process value to be used in catalog query
        """
        if isinstance(value, (tuple, list)):
            value = self.normalize_list(value)
        elif isinstance(value, (str, unicode)):
            value = self.normalize_string(value)
        return value

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

        value = self.normalize(value)
        query[index] = {'query': value, 'operator': 'and'}
        return query
