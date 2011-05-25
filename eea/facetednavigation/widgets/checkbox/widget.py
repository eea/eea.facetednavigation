""" Checkbox widget
"""
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.utils import DisplayList

from eea.faceted.vocabularies.utils import compare
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _


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
            i18n_domain="eea"
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
            i18n_domain="eea"
        )
    ),
    StringField('vocabulary',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
        widget=SelectionWidget(
            label=_('faceted_criteria_vocabulary', default=u"Vocabulary"),
            description=_('help_faceted_criteria_vocabulary',
                          default=u'Vocabulary to use to render widget items'),
        )
    ),
    StringField('catalog',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.UseCatalog',
        widget=SelectionWidget(
            format='select',
            label=_('faceted_criteria_catalog', default=u'Catalog'),
            label_msgid='faceted_criteria_catalog',
            description=_('help_faceted_criteria_catalog',
                          default=u"Get unique values from catalog "
                                  u"as an alternative for vocabulary"),
        )
    ),
    IntegerField('maxitems',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label=_('faceted_criteria_maxitems', default=u"Maximum items"),
            description=_('help_faceted_criteria_maxitems',
                          default=u'Number of items visible in widget'),
        )
    ),
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label=_('faceted_criteria_reverse_options',
                    default=u"Reverse options"),
            description=_('help_faceted_criteria_reverse_options',
                          default=u"Sort options reversed"),
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label=_('faceted_criteria_count', default=u"Count results"),
            description=_('help_faceted_criteria_count',
                         default=u"Display number of results near each option"),
        )
    ),
    BooleanField('hidezerocount',
        schemata="countable",
        widget=BooleanWidget(
            label='Hide items with zero results',
            label_msgid='faceted_criteria_emptycounthide',
            description='This option works only if "count results" is enabled',
            description_msgid='help_faceted_criteria_criteria_emptycounthide',
            i18n_domain="eea"
        )
    ),
    LinesField('default',
        schemata="default",
        widget=LinesWidget(
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default items (one per line)',
            description_msgid='help_faceted_criteria_checkboxes_default',
            i18n_domain="eea"
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'checkbox'
    widget_label = _('Checkboxes')
    view_js = '++resource++eea.facetednavigation.widgets.checkbox.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.checkbox.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.checkbox.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.checkbox.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema.copy() + EditSchema

    @property
    def default(self):
        """ Get default values
        """
        default = super(Widget, self).default
        if not default:
            return []

        if isinstance(default, (str, unicode)):
            default = [default, ]
        return default

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

