""" Solr tests
"""
from eea.facetednavigation.tests.base import FacetedTestCase
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation.widgets.widget import Widget
from eea.facetednavigation.widgets.autocomplete.widget import Widget as AWidget

class DummySolrResponse(dict):
    """ Solr
    """
    @property
    def facet_counts(self):
        """ Count
        """
        return {'facet_fields': self}


class CountableWidgetTestCase(FacetedTestCase):
    """ Test
    """
    def afterSetUp(self):
        """ Setup
        """
        self.request = self.app.REQUEST

    def test_widget_empty_count(self):
        """ Empty count
        """
        data = {}
        widget = CountableWidget(self.portal, self.request, data=data)
        self.assertEqual(widget.count([]), {})

    def test_widget_solr_count(self):
        """ Test facet extraction from solr response
        """
        data = {'index': 'tags'}
        widget = CountableWidget(self.portal, self.request, data=data)
        dummyresponse = DummySolrResponse({'tags': {'foo': 10, 'bar': 7}})
        self.assertEqual(widget.count(dummyresponse),
                         {'': 1, 'all': 1, u'bar': 7, u'foo': 10})


class WidgetTestCase(FacetedTestCase):
    """ Test
    """

    def afterSetUp(self):
        """ Setup
        """
        self.request = self.app.REQUEST

    def test_default_from_widget(self):
        """ Get default value from widget.
        """
        data = {'index': 'SearchableText', 'default': 'fun'}
        self.request.form['otherindex'] = 'serious fun'
        widget = Widget(self.portal, self.request, data=data)
        self.assertEqual(widget.default, 'fun')

    def test_default_from_request(self):
        """ Get default value from request.
        """
        data = {'index': 'SearchableText', 'default': 'fun'}
        self.request.form['SearchableText'] = 'serious fun'
        widget = Widget(self.portal, self.request, data=data)
        self.assertEqual(widget.default, 'serious fun')



class AutocompleteWidgetTestCase(FacetedTestCase):
    """ Test
    """

    def afterSetUp(self):
        """ Setup
        """
        self.request = self.app.REQUEST

    def test_comma_separated_values(self):
        """ Comma separated values are transformed to a list
        """
        data = {}
        value = 'Folder,Document'
        widget = AWidget(self.portal, self.request, data=data)
        self.assertEqual(widget.normalize(value), ['Folder', 'Document'])
