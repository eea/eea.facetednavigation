""" Text widget
"""
import logging
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.CMFCore.utils import getToolByName

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _


logger = logging.getLogger('eea.facetednavigation.widgets.range')

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.RangeCatalogIndexes',
        widget=SelectionWidget(
            format='select',
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
            description=_(u"Default range (e.g. '1 => 3')"),
            i18n_domain="eea"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'range'
    widget_label = _('Range')
    view_js = '++resource++eea.facetednavigation.widgets.range.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.range.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.range.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.range.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema

    @property
    def default(self):
        """ Return default
        """
        default = self.data.get('default', '')
        if not default:
            return ('', '')

        default = default.split('=>')
        if len(default) != 2:
            return ('', '')

        start, end = default
        return (start, end)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            start, end = self.default
        else:
            value = form.get(self.data.getId(), ())
            if not value or len(value) != 2:
                return query
            start, end = value

        if not (start and end):
            return query

        # let the field be integer if integer:
        catalog = getToolByName(self.context, 'portal_catalog')
        evalues = catalog.uniqueValuesFor(index)
        if True in [isinstance(v, int) for v in evalues]:
            start, end = int(start), int(end)
        query[index] = {
            'query': (start, end),
            'range': 'min:max'
        }
        return query


