""" Widget
"""
import logging
from Products.CMFCore.utils import getToolByName

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.range.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.range.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _
logger = logging.getLogger('eea.facetednavigation.widgets.range')


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'range'
    widget_label = _('Range')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')

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
