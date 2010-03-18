""" Checkbox widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.utils import DisplayList
from eea.facetednavigation.widgets.field import StringField

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from eea.faceted.vocabularies.utils import compare
from eea.facetednavigation.widgets.widget import CountableWidget


EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.CatalogIndexes',
        widget=SelectionWidget(
            label='Catalog index',
            label_msgid='faceted_criteria_index',
            description='Catalog index to use for search',
            description_msgid='help_faceted_criteria_index',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('operator',
        schemata='default',
        required=True,
        vocabulary=DisplayList([('or', 'OR'), ('and', 'AND')]),
        default='or',
        widget=SelectionWidget(
            format='select',
            label='Operator',
            label_msgid='faceted_criteria_operator',
            description='Search with AND/OR between elements',
            description_msgid='help_faceted_criteria_operator',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('vocabulary',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
        widget=SelectionWidget(
            label='Vocabulary',
            label_msgid='faceted_criteria_vocabulary',
            description='Vocabulary to use to render widget items',
            description_msgid='help_faceted_criteria_vocabulary',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('catalog',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.UseCatalog',
        widget=SelectionWidget(
            format='select',
            label='Catalog',
            label_msgid='faceted_criteria_catalog',
            description='Get unique values from catalog as an alternative for vocabulary',
            description_msgid='help_faceted_criteria_catalog',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('maxitems',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label='Maximum items',
            label_msgid='faceted_criteria_maxitems',
            description='Number of items visible in widget',
            description_msgid='help_faceted_criteria_maxitems',
            i18n_domain="eea.facetednavigation"
        )
    ),
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label='Reverse options',
            label_msgid='faceted_criteria_reverse_options',
            description='Sort options reversed',
            description_msgid='help_faceted_criteria_reverse_options',
            i18n_domain="eea.facetednavigation"
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label='Count results',
            label_msgid='faceted_criteria_count',
            description='Display number of results near each option',
            description_msgid='help_faceted_criteria_count',
            i18n_domain="eea.facetednavigation"
        )
    ),
    BooleanField('hidezerocount',
        schemata="countable",
        widget=BooleanWidget(
            label='Hide items with zero results',
            label_msgid='faceted_criteria_emptycounthide',
            description='This option works only if "count results" is enabled',
            description_msgid='help_faceted_criteria_criteria_emptycounthide',
            i18n_domain="eea.facetednavigation"
        )
    ),
    LinesField('default',
        schemata="default",
        widget=LinesWidget(
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default items (one per line)',
            description_msgid='help_faceted_criteria_checkboxes_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'checkbox'
    widget_label = 'Checkboxes'
    view_js = '++resource++eea.facetednavigation.widgets.checkbox.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.checkbox.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.checkbox.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.checkbox.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema + EditSchema

    def selected(self, key):
        """ Return True if key in self.default
        """
        if not self.default:
            return False
        for item in self.default:
            if compare(key, item) == 0:
                return True
        return False

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')

        # Use 'and' by default in order to be backward compatible
        operator = self.data.get('operator', 'and')
        operator = operator.encode('utf-8', 'replace')

        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        if not value:
            return query

        query[index] = {'query': value, 'operator': operator}
        return query

