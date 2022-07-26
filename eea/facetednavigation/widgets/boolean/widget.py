""" Checkbox widget
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.boolean.interfaces import CountableSchemata
from eea.facetednavigation.widgets.boolean.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.boolean.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.widget import CountableWidget
from plone.i18n.normalizer import urlnormalizer as normalizer


class Widget(CountableWidget):
    """Widget"""

    # Widget properties
    widget_type = "boolean"
    widget_label = _("Boolean")
    groups = (DefaultSchemata, LayoutSchemata, CountableSchemata)

    index = ViewPageTemplateFile("widget.pt")

    @property
    def css_class(self):
        """Widget specific css class"""
        css_type = self.widget_type
        css_title = normalizer.normalize(self.data.title)
        return (
            "faceted-checkboxes-widget " "faceted-{0}-widget section-{1}{2}"
        ).format(css_type, css_title, self.custom_css)

    def selected(self):
        """Return True if True by default"""
        return self.default or False

    def vocabulary(self, **kwargs):
        """Vocabulary"""
        return [(1, 1)]

    def index_id(self):
        """Index"""
        return self.data.get("index", "").lower()

    def query(self, form):
        """Get value from form and return a catalog dict query"""
        index = self.data.get("index", "")
        if not index:
            return {}

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), "")

        if value:
            return {index: True}
        return {}
