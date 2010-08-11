""" Text widget
"""
import logging
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
logger = logging.getLogger('eea.facetednavigation.widgets.portlet')

EditSchema = Schema((
    StringField('macro',
        schemata="default",
        required=True,
        widget=StringWidget(
            label='Portlet macro',
            label_msgid='faceted_portlet_macro',
            description='Path to portlet macro',
            description_msgid='help_faceted_portlet_macro',
            i18n_domain="eea.facetednavigation"
        )
    )
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'portlet'
    widget_label = 'Plone portlet'
    view_js = '++resource++eea.facetednavigation.widgets.portlet.view.js'
    view_css = '++resource++eea.facetednavigation.widgets.portlet.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.portlet.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'Portlet'

    @property
    def macro(self):
        """ Get macro
        """
        macro = self.data.get('macro', '')
        if not macro:
            raise ValueError('Empty macro %s' % macro)

        macro_list = macro.replace('here/', '', 1)
        macro_list = macro_list.split('/macros/')
        if len(macro_list) != 2:
            raise ValueError('Invalid macro: %s' % macro)

        path, mode = macro_list
        path = path.split('/')
        try:
            template = self.context.restrictedTraverse(path)
            if template:
                return template.macros[mode]
        except Exception, err:
            # This means we didn't have access or it doesn't exist
            raise
        raise ValueError("Invalid macro: %s" % macro)
