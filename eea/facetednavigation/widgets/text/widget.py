""" Text widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringWidget
from eea.facetednavigation.widgets.field import StringField
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

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

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema + EditSchema

    def tokenize_string(self, value):
        """ Process string values to be used in catalog query
        """
        return value.split()

    def tokenize_list(self, value):
        """ Process list values to be used in catalog query
        """
        words = []
        for word in value:
            words.extend(self.tokenize_string(word))
        return words

    def tokenize(self, value):
        """ Process value to be used in catalog query
        """
        if isinstance(value, (tuple, list)):
            value = self.tokenize_list(value)
        elif isinstance(value, (str, unicode)):
            value = self.tokenize_string(value)

        # Ensure words are string instances as ZCatalog requires strings
        words = []
        for word in value:
            if isinstance(word, unicode):
                word = word.encode('utf-8')
            words.append(word)
        return words

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

        ctool = getToolByName(self.context, 'portal_catalog')
        catalog_index = ctool._catalog.getIndex(index)
        if getattr(catalog_index, 'meta_type', '') == 'ZCTextIndex':
            value = self.tokenize(value)
        else:
            # Ensure words are string instances as ZCatalog requires strings
            if isinstance(value, str):
                value = value.decode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')

        query[index] = {'query': value, 'operator': 'and'}
        return query
