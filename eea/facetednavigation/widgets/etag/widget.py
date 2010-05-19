""" ETag widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from eea.facetednavigation.widgets.field import StringField

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

EditSchema = Schema((
    StringField('default',
        schemata="default",
        default='1.0',
        widget=StringWidget(
            size=25,
            label='Default etag',
            label_msgid='faceted_criteria_etag_default',
            description='Etag value',
            description_msgid='help_faceted_criteria_etag_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'etag'
    widget_label = 'ETag'
    edit_js = '++resource++eea.facetednavigation.widgets.etag.edit.js'
    edit_css = '++resource++eea.facetednavigation.widgets.etag.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'ETag'
    edit_schema['hidden'].default = True
    edit_schema['hidden'].schemata = 'hidden'
