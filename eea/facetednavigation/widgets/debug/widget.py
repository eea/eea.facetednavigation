""" Widget
"""
from zope.component import getUtility
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import DisplayList

from eea.facetednavigation.widgets.field import StringField
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

EditSchema = Schema((
    StringField('user',
        schemata="default",
        required=True,
        vocabulary=DisplayList(()),
        widget=SelectionWidget(
            format='select',
            label='Visible to',
            label_msgid='faceted_criteria_user',
            description='Widget will be visible only for selected user',
            description_msgid='help_faceted_criteria_user',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'debug'
    widget_label = 'Debugger'
    view_css = '++resource++eea.facetednavigation.widgets.debug.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.debug.edit.css'
    edit_js = '++resource++eea.facetednavigation.widgets.debug.edit.js'
    view_js = '++resource++eea.facetednavigation.widgets.debug.view.js'
    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema.copy()
    edit_schema['title'].default = 'Debug faceted criteria'

    def __init__(self, context, request, data=None):
        super(Widget, self).__init__(context, request, data)

        voc = getUtility(IVocabularyFactory, 'eea.faceted.vocabularies.CurrentUser')
        voc = [(term.value, term.title or term.value) for
               term in voc(context) if term.value]
        self.edit_schema['user'].vocabulary = DisplayList(voc)
