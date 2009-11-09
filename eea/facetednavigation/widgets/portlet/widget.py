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
    edit_js = '++resource++eea.facetednavigation.widgets.portlet.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.portlet.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.portlet.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    edit_schema = AbstractWidget.edit_schema + EditSchema

    @property
    def macro(self):
        """ Get macro
        """
        macro = self.data.get('macro', '')
        if not macro:
            return ''

        macro = macro.replace('here/', '', 1)
        macro = macro.split('/macros/')
        if len(macro) != 2:
            return ''

        path, mode = macro
        path = path.split('/')
        try:
            template = self.context.restrictedTraverse(path)
            if template:
                return template.macros[mode]
        except Exception, err:
            # This means we didn't have access or it doesn't exist
            logger.exception('macro: %s, error: %s', macro, err)
            return ''
        logger.exception("Macro %s does not exist", macro)
        return ''
