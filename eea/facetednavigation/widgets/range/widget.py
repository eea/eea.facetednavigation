""" Widget
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.range.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.range.interfaces import DisplaySchemata
from eea.facetednavigation.widgets.range.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

import logging


logger = logging.getLogger("eea.facetednavigation")


class Widget(AbstractWidget):
    """Widget"""

    widget_type = "range"
    widget_label = _("Range")

    groups = (DefaultSchemata, LayoutSchemata, DisplaySchemata)
    index = ViewPageTemplateFile("widget.pt")

    @property
    def default(self):
        """Return default"""
        default = self.data.get("default", "")
        if not default:
            return ("", "")

        default = default.split("=>")
        if len(default) != 2:
            return ("", "")

        start, end = default
        return (start, end)

    @property
    def integer(self):
        """Integer only"""
        return self.data.get("integer", False)

    def query(self, form):
        """Get value from form and return a catalog dict query"""
        query = {}
        index = self.data.get("index", "")
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
        try:
            _start = int(float(start))
        except ValueError:
            _start = start

        try:
            _end = int(float(end))
        except ValueError:
            _end = end

        query[index] = {"query": (_start, _end), "range": "min:max"}
        return query
