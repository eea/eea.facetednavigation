""" Widget
"""
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.text.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.text.interfaces import DefaultSchemata


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'text'
    widget_label = _('Text field')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')

    def quotestring(self, string):
        """ Quote given string
        """
        return '"%s"' % string

    def quote_bad_chars(self, string):
        """ Quote bad chars in query string
        """
        bad_chars = ["(", ")"]
        for char in bad_chars:
            string = string.replace(char, self.quotestring(char))
        return string

    def normalize_string(self, value):
        """ Process string values to be used in catalog query
        """
        # Ensure words are string instances as ZCatalog requires strings
        if isinstance(value, str):
            value = value.decode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if self.data.get('wildcard', False) and not value.endswith("*"):
            value = value + "*"
        value = self.quote_bad_chars(value)
        return value

    def normalize_list(self, value):
        """ Process list values to be used in catalog query
        """
        return [self.normalize_string(word) for word in value]

    def normalize(self, value):
        """ Process value to be used in catalog query
        """
        if isinstance(value, (tuple, list)):
            value = self.normalize_list(value)
        elif isinstance(value, (str, unicode)):
            value = self.normalize_string(value)
        return value

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        if not value:
            return query

        value = self.normalize(value)
        query[index] = {'query': value, 'operator': 'and'}
        return query
