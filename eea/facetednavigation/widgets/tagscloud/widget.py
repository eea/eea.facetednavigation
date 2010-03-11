""" Checkbox widget
"""
import random
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget
from eea.facetednavigation.widgets.field import StringField
from eea.faceted.vocabularies.utils import compare

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import CountableWidget

TagsCloudTypes = DisplayList((
    ("list", "List"),
    ("sphere", "Sphere"),
    ("cloud", "Cloud"),
))

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
        default=50,
        widget=IntegerWidget(
            label='Maximum items',
            label_msgid='faceted_criteria_maxitems',
            description='Number of items visible in widget',
            description_msgid='help_faceted_criteria_maxitems',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('maxchars',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label='Maximum characters',
            label_msgid='faceted_criteria_maxchars',
            description='Cut long phrases to provided number of characters',
            description_msgid='help_faceted_criteria_maxchars',
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
    StringField('cloud',
        schemata="geometry",
        vocabulary=TagsCloudTypes,
        widget=SelectionWidget(
            format='select',
            label='Cloud type',
            label_msgid='faceted_criteria_tagscloud_type',
            description='Type of the cloud',
            description_msgid='help_faceted_criteria_tagscloud_type',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('sizemin',
        schemata="geometry",
        default=10,
        widget=IntegerWidget(
            label='Minimum size',
            label_msgid='faceted_criteria_tagscloud_minsize',
            description='Minimum font-size (px)',
            description_msgid='help_faceted_criteria_tagscloud_minsize',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('sizemax',
        schemata="geometry",
        default=20,
        widget=IntegerWidget(
            label='Maximum size',
            label_msgid='faceted_criteria_tagscloud_maxsize',
            description='Maximum font-size (px)',
            description_msgid='help_faceted_criteria_tagscloud_maxsize',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('height',
        schemata="geometry",
        default=200,
        widget=IntegerWidget(
            label='Cloud height',
            label_msgid='faceted_criteria_tagscloud_height',
            description='Cloud height (px)',
            description_msgid='help_faceted_criteria_tagscloud_height',
            i18n_domain="eea.facetednavigation"
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label='Count results',
            label_msgid='faceted_criteria_count',
            description='Display number of results near each tag',
            description_msgid='help_faceted_criteria_tagscloud_count',
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
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default selected item',
            description_msgid='help_faceted_criteria_radio_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'tagscloud'
    widget_label = 'Tags Cloud'
    view_js = '++resource++eea.facetednavigation.widgets.tagscloud.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.tagscloud.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.tagscloud.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.tagscloud.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema + EditSchema

    @property
    def maxitems(self):
        maxitems = self.data.get('maxitems', 0)
        try:
            maxitems = int(maxitems)
        except (ValueError, TypeError), err:
            maxitems = 0
        return maxitems

    def cut_text(self, text='', maxchars=0):
        """ Cut long text
        """
        if not maxchars:
            maxchars = self.data.get('maxchars', 0)

        try:
            maxchars = int(maxchars)
        except (ValueError, TypeError):
            maxchars = 0

        if not maxchars:
            return text

        # Allow 20 % more characters in order
        # to avoid cutting at the end of the text
        if len(text) <= (maxchars + round(0.2 * maxchars)):
            return text
        return '%s...' % text[0:maxchars]

    def vocabulary(self, all=False):
        """ Return a limited number of results
        """
        voc = super(Widget, self).vocabulary()

        if all:
            maxitems = 0
        else:
            maxitems = self.maxitems

        voc.insert(0, ('all', 'All'))
        for index, item in enumerate(voc):
            if maxitems and (index >= maxitems):
                raise StopIteration
            res = (item[0], item[1], -1)
            yield res

    @property
    def randint(self):
        maxint = self.maxitems or 100
        return random.randint(0, maxint)

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

        if compare(value, 'all') == 0:
            return query

        if not isinstance(value, unicode):
            value = value.decode('utf-8')

        query[index] = value.encode('utf-8')
        return query

    def __call__(self, **kwargs):
        return self.index(kwargs=kwargs)
