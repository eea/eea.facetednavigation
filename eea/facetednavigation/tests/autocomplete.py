""" Autocomplete widget tests
"""
import json
from Products.Five import BrowserView
from zope.interface import implementer

from eea.facetednavigation.vocabularies.autocomplete import IAutocompleteSuggest

vocab = [
    ("Document", "Document"),
    ("Event", "Event"),
    ("Folder", "Folder"),
]


@implementer(IAutocompleteSuggest)
class TypesSuggest(BrowserView):
    """Types Autocomplete view"""

    label = "Types"

    def __call__(self):
        result = []
        query = self.request.get("term")
        if not query:
            return json.dumps(result)

        self.request.response.setHeader("Content-type", "application/json")
        for term in vocab:
            if term[1].lower().startswith(query.lower()):
                result.append({"id": term[0], "text": term[1]})

        return json.dumps(result)
