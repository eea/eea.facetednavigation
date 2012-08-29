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
            label=_(u'Catalog index'),
            description=_(u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    StringField('vocabulary',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
        widget=SelectionWidget(
            label=_(u'Vocabulary'),
            description=_(u'Vocabulary to use to render widget items'),
            i18n_domain="eea"
        )
    ),
    StringField('catalog',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.UseCatalog',
        widget=SelectionWidget(
            format='select',
            label=_(u'Catalog'),
            description=_(u'Get unique values from catalog as an alternative '
                        u'for vocabulary'),
            i18n_domain="eea"
        )
    ),
    IntegerField('maxitems',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label=_(u'Maximum items'),
            description=_(u'Number of items visible in widget'),
            i18n_domain="eea"
        )
    ),
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label=_(u'Reverse options'),
            description=_(u'Sort options reversed'),
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_(u'Default value'),
            description=_(u'Default selected item'),
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
