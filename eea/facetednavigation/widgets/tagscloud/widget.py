""" Tag-Cloud widget
"""
import random
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget
from Products.CMFPlone.utils import safeToInt
from eea.faceted.vocabularies.utils import compare

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _

TagsCloudTypes = DisplayList((
    ("list", _("List")),
    ("sphere", _("Sphere")),
    ("cloud", _("Cloud")),
))

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.CatalogIndexes',
        widget=SelectionWidget(
            label=_(u'faceted_criteria_index',
                default='Catalog index'),
            description=_(u'help_faceted_criteria_index',
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
            description=_(u'help_faceted_criteria_vocabulary',
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
        default=50,
        widget=IntegerWidget(
            label=_(u'faceted_criteria_maxitems',
                default=u'Maximum items'),
            description=_(u'help_faceted_criteria_maxitems',
                default=u'Number of items visible in widget'),
            i18n_domain="eea"
        )
    ),
    IntegerField('maxchars',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label=_(u'faceted_criteria_maxchars',
                default=u'Maximum characters'),
            description=_(u'help_faceted_criteria_maxchars',
                default=u'Cut long phrases to provided number of characters'),
            i18n_domain="eea"
        )
    ),
    StringField('colormin', 
        schemata="display", 
        default="A1BE7E", 
        widget=StringWidget( 
            label='Minimum color', 
            label_msgid='faceted_criteria_colormin', 
            description='Tagscloud minimum color', 
            description_msgid='help_faceted_criteria_colormin', 
            i18n_domain="eea.facetednavigation" 
        ) 
    ), 
    StringField('colormax', 
        schemata="display", 
        default="95B229", 
        widget=StringWidget( 
            label='Maximum color', 
            label_msgid='faceted_criteria_colormax', 
            description='Tagscloud max color', 
            description_msgid='help_faceted_criteria_colormax', 
            i18n_domain="eea.facetednavigation" 
        ) 
    ), 
    BooleanField('sortreversed',
        schemata="display",
        widget=BooleanWidget(
            label=_(u'faceted_criteria_reverse_options',
                default=u'Reverse options'),
            description=_(u'help_faceted_criteria_reverse_options',
                default=u'Sort options reversed'),
            i18n_domain="eea"
        )
    ),
    StringField('cloud',
        schemata="geometry",
        vocabulary=TagsCloudTypes,
        widget=SelectionWidget(
            format='select',
            label=_(u'faceted_criteria_tagscloud_type',
                default='Cloud type'),
            description=_(u'help_faceted_criteria_tagscloud_type',
                default=u'Type of the cloud'),
            i18n_domain="eea"
        )
    ),
    IntegerField('sizemin',
        schemata="geometry",
        default=10,
        widget=IntegerWidget(
            label=_('faceted_criteria_tagscloud_minsize',
                default=u'Minimum size'),
            description=_(u'help_faceted_criteria_tagscloud_minsize',
                default=u'Minimum font-size (px)'),
            i18n_domain="eea"
        )
    ),
    IntegerField('sizemax',
        schemata="geometry",
        default=20,
        widget=IntegerWidget(
            label=_(u'faceted_criteria_tagscloud_maxsize',
                default=u'Maximum size'),
            description=_(u'help_faceted_criteria_tagscloud_maxsize',
                default=u'Maximum font-size (px)'),
            i18n_domain="eea"
        )
    ),
    IntegerField('height',
        schemata="geometry",
        default=200,
        widget=IntegerWidget(
            label=_(u'faceted_criteria_tagscloud_height',
                default=u'Cloud height'),
            description=_(u'help_faceted_criteria_tagscloud_height',
                default=u'Cloud height (px)'),
            i18n_domain="eea"
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label=_('faceted_criteria_count', default=u'Count results'),
            description=_('help_faceted_criteria_tagscloud_count',
                          default=u"Display number of results near each tag"),
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
            label=_('faceted_criteria_default',
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
    widget_type = 'tagscloud'
    widget_label = _('Tags Cloud')
    view_js = '++resource++eea.facetednavigation.widgets.tagscloud.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.tagscloud.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.tagscloud.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.tagscloud.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema.copy() + EditSchema

    @property
    def maxitems(self):
        """ Maximum items
        """
        return safeToInt(self.data.get('maxitems', 0))

    def cut_text(self, text='', maxchars=0):
        """ Cut long text
        """
        maxchars = safeToInt(self.data.get('maxchars', 0))
        if not maxchars:
            return text

        # Allow 20 % more characters in order
        # to avoid cutting at the end of the text
        if len(text) <= (maxchars + round(0.2 * maxchars)):
            return text
        return '%s...' % text[0:maxchars]

    def vocabulary(self, oll=False):
        """ Return a limited number of results
        """
        voc = list(super(Widget, self).vocabulary())

        if oll:
            maxitems = 0
        else:
            maxitems = self.maxitems

        voc.insert(0, ('all', 'All'))
        for index, item in enumerate(voc):
            if maxitems and (index >= maxitems):
                return
            res = (item[0], item[1], -1)
            yield res

    @property
    def randint(self):
        """ Random integer
        """
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
