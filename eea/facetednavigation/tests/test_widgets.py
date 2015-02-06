from eea.facetednavigation.tests.base import FacetedTestCase
from eea.facetednavigation.widgets.widget import CountableWidget


class DummySolrResponse(dict):

    @property
    def facet_counts(self):
        class DummyCounts(dict):
           @property
           def facet_fields(self):
               return self.items()
        return DummyCounts(self)


class CountableWidgetTestCase(FacetedTestCase):

    def afterSetUp(self):
        self.request = self.app.REQUEST

    def test_widget_empty_count(self):
        data = {}
        widget = CountableWidget(self.portal, self.request, data=data)
        self.assertEqual(widget.count([]), {})

    def test_widget_solr_count(self):
        """ Test facet extraction from solr response """
        data = {}
        widget = CountableWidget(self.portal, self.request, data=data)
        dummyresponse = DummySolrResponse({'foo': 10, 'bar': 7})
        self.assertEqual(widget.count(dummyresponse),
                         {'': 2, 'all': 2, u'bar': 7, u'foo': 10})
