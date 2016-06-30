""" Widget
"""
import logging
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.portlet.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.portlet.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _

logger = logging.getLogger('eea.facetednavigation.widgets.portlet')

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'portlet'
    widget_label = _('Plone portlet')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ZopeTwoPageTemplateFile('widget.pt', globals())

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
            template = getattr(template, 'index', template)
            if template:
                return template.macros[mode]
        except Exception:
            # This means we didn't have access or it doesn't exist
            raise
        raise ValueError("Invalid macro: %s" % macro)
