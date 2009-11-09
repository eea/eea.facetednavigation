""" Text widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from eea.facetednavigation.widgets.field import StringField

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.TextCatalogIndexes',
        widget=SelectionWidget(
            label='Catalog index',
            label_msgid='faceted_criteria_index',
            description='Catalog index to use for search',
            description_msgid='help_faceted_criteria_index',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default string to search for',
            description_msgid='help_faceted_criteria_text_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'text'
    widget_label = 'Text field'
    view_js = '++resource++eea.facetednavigation.widgets.text.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.text.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.text.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.text.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema + EditSchema

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

        query[index] = {'query': value, 'operator': 'and'}
        return query
