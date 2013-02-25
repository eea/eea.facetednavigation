""" ETag widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _

EditSchema = Schema((
    StringField('default',
        schemata="default",
        default='1.0',
        widget=StringWidget(
            size=25,
            label=_(u'Default etag'),
            description=_(u'Etag value'),
            i18n_domain="eea"
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
