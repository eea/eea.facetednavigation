""" Autocomplete widget tests
"""
import json
from Products.Five import BrowserView
from zope.interface import implements

from eea.faceted.vocabularies.autocomplete import IAutocompleteSuggest

vocab = [
    ('Document', u"Document"),
    ('Event', u"Event"),
    ('Folder', u"Folder"),
]

class TypesSuggest(BrowserView):
    """ Types Autocomplete view """
    implements(IAutocompleteSuggest)

    label = u"Types"

    def __call__(self):
        result = []
        query = self.request.get('term')
        if not query:
            return json.dumps(result)

        self.request.response.setHeader("Content-type", "application/json")
        for term in vocab:
            if term[1].lower().startswith(query.lower()):
                result.append({'id': term[0], 'text': term[1]})

        return json.dumps(result)
