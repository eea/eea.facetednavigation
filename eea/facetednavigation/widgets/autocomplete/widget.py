""" Widget
"""
import json
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
from zope.interface import implementer
from zope.component import queryUtility

from lxml import etree

from Products.Five import BrowserView

from eea.facetednavigation.vocabularies.autocomplete import IAutocompleteSuggest
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.autocomplete.interfaces import ISolrConnectionManager
from eea.facetednavigation.widgets.autocomplete.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.autocomplete.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.autocomplete.interfaces import DisplaySchemata
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
import six


class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'autocomplete'
    widget_label = _('Text field with suggestions')

    index = ViewPageTemplateFile('widget.pt')
    groups = (DefaultSchemata, LayoutSchemata, DisplaySchemata)

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
        if isinstance(value, six.binary_type):
            value = value.decode('utf-8')
        if six.PY2 and isinstance(value, six.text_type):
            value = value.encode('utf-8')
        value = self.quote_bad_chars(value)
        return value

    def normalize_list(self, value):
        """ Process list values to be used in catalog query
        """
        return [self.normalize_string(word) for word in value]

    def normalize(self, value):
        """ Process value to be used in catalog query
        """
        # select2 send us selected values separated by a comma
        if ',' in value:
            value = value.split(',')
        if isinstance(value, (tuple, list)):
            value = self.normalize_list(value)
        elif isinstance(value, (six.binary_type, six.text_type)):
            value = self.normalize_string(value)
        return value

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        if six.PY2:
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

    def autocomplete_view(self):
        """ Get the autocomplete view name
        """
        view_name = self.data.get('autocomplete_view', '')
        return view_name


@implementer(IAutocompleteSuggest)
class SolrSuggest(BrowserView):
    """ Solr Autocomplete view
    """
    label = _("solr")

    def __call__(self):
        result = []
        term = self.request.get('term')
        manager = queryUtility(ISolrConnectionManager)
        if not manager or not term:
            return json.dumps(result)

        connection = manager.getConnection()
        if not connection:
            return json.dumps(result)

        # XXX this should really go into c.solr
        request = six.moves.urllib.parse.urlencode({'q': term}, doseq=True)
        response = connection.doPost(
            connection.solrBase + '/suggest', request, connection.formheaders)
        root = etree.fromstring(response.read())
        suggestion = root.xpath("//arr[@name='suggestion']")
        if suggestion:
            suggestions = suggestion[0].findall('str')
            result = [{'id': s.text, 'text': s.text} for s in suggestions]

        return json.dumps(result)
