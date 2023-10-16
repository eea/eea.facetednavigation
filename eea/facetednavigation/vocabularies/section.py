""" Widget Sections Vocabularies
"""
from eea.facetednavigation import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class WidgetSections(object):
    """Widget position in page"""

    def __call__(self, *args, **kwargs):
        items = (
            SimpleTerm("default", "default", _("Basic search")),
            SimpleTerm("advanced", "advanced", _("Extended search")),
        )
        return SimpleVocabulary(items)
