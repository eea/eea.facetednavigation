""" Checkbox widget
"""
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget

from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _


EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.CatalogIndexes',
        widget=SelectionWidget(
            label=_(u'faceted_criteria_index',
                default=u'Catalog index'),
            description=_('help_faceted_criteria_index',
                default=u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    StringField('vocabulary',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
        widget=SelectionWidget(
            label=_(u'faceted_criteria_vocabulary',
                default=u'Vocabulary'),
            description=_('help_faceted_criteria_vocabulary',
                default=u'Vocabulary to use to render widget items'),
            i18n_domain="eea"
        )
    ),
    StringField('catalog',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.UseCatalog',
        widget=SelectionWidget(
            format='select',
            label=_(u'faceted_criteria_catalog',
                default=u'Catalog'),
            description=_(u'help_faceted_criteria_catalog',
                default=u'Get unique values from catalog as an alternative '
                        u'for vocabulary'),
            i18n_domain="eea"
        )
    ),
    IntegerField('maxitems',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label=_(u'faceted_criteria_maxitems',
                default='Maximum items'),
            description=_(u'help_faceted_criteria_maxitems',
                default=u'Number of items visible in widget'),
            i18n_domain="eea"
        )
    ),
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label=_(u'faceted_criteria_reverse_options',
                default='Reverse options'),
            description=_(u'help_faceted_criteria_reverse_options',
                default='Sort options reversed'),
            i18n_domain="eea"
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label=_(u'faceted_criteria_count', default=u'Count results'),
            description=_('help_faceted_criteria_count',
                default=u'Display number of results near each option'),
            i18n_domain="eea"
        )
    ),
    BooleanField('hidezerocount',
        schemata="countable",
        widget=BooleanWidget(
            label=_(u'faceted_criteria_emptycounthide',
                default=u'Hide items with zero results'),
            description=_(u'help_faceted_criteria_criteria_emptycounthide',
               default=u'This option works only if "count results" is enabled'),
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_(u'faceted_criteria_default',
                default=u'Default value'),
            description=_(u'help_faceted_criteria_radio_default',
                default=u'Default selected item'),
            i18n_domain="eea"
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'radio'
    widget_label = _('Radio')
    view_js = '++resource++eea.facetednavigation.widgets.radio.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.radio.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.radio.view.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema.copy() + EditSchema

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

        if not isinstance(value, unicode):
            value = value.decode('utf-8')

        query[index] = value.encode('utf-8')
        return query
