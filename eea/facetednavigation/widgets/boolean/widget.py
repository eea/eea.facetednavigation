""" Checkbox widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _


BooleanEditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.SimpleFieldCatalogIndexes',
        widget=SelectionWidget(
            label=_(u'Catalog index'),
            description=_(u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    BooleanField('default',
        schemata="default",
        widget=BooleanWidget(
            label=_(u'Default value'),
            description=_(u'Default items (one per line)'),
            i18n_domain="eea"
        )
    ),
))

BooleanEditSchema = CountableWidget.edit_schema.copy() + BooleanEditSchema
del BooleanEditSchema['sortcountable']
del BooleanEditSchema['hidezerocount']

class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'boolean'
    widget_label = _('Boolean')
    view_js = '++resource++eea.facetednavigation.widgets.checkbox.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.checkbox.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.checkbox.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.checkbox.edit.css'
    edit_schema = BooleanEditSchema
    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Get default values
        """
        return bool(self.data.get('default', None))

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
