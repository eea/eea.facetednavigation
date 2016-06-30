""" Widget
"""
import logging
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.resultsperpage.interfaces import (
    DefaultSchemata,
    LayoutSchemata,
    DisplaySchemata,
)
logger = logging.getLogger('eea.facetednavigation.widgets.resultsperpage')


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'resultsperpage'
    widget_label = _('Results per page')

    groups = (DefaultSchemata, LayoutSchemata, DisplaySchemata)
    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Get default values
        """
        value = self.data.get('default', 0) or 0
        try:
            return int(value)
        except (TypeError, ValueError), err:
            logger.exception(err)
            return 0

    def results_per_page(self, form, default=20):
        """ Get results per page
        """
        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), default)

        if not value:
            return default

        try:
            value = int(value)
        except (TypeError, ValueError), err:
            logger.exception(err)
            return default

        return value

    def vocabulary(self, **kwargs):
        """ Vocabulary
        """
        try:
            start = int(self.data.get('start', 0) or 0)
        except (TypeError, ValueError), err:
            logger.exception(err)
            start = 0
        try:
            end = int(self.data.get('end', 21)) + 1
        except (TypeError, ValueError), err:
            logger.exception(err)
            end = 21
        try:
            step = int(self.data.get('step', 1))
        except (TypeError, ValueError), err:
            logger.exception(err)
            step = 1

        return [(x, x) for x in range(start, end, step)]
