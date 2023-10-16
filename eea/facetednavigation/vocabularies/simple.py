""" Simple static vocabularies
"""
from eea.facetednavigation import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


#
# Use catalog
#
@implementer(IVocabularyFactory)
class UseCatalogVocabulary(object):
    """Use catalog vocabulary"""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        items = (
            SimpleTerm("", "", _("No")),
            SimpleTerm("portal_catalog", "portal_catalog", _("Yes")),
        )
        return SimpleVocabulary(items)


#
# JsTree themes
#
@implementer(IVocabularyFactory)
class JsTreeThemes(object):
    """Widget position in page"""

    def __call__(self, *args, **kwargs):
        items = (
            SimpleTerm("default", "default", _("Default")),
            SimpleTerm("classic", "classic", _("Classic")),
            SimpleTerm("apple", "apple", _("Apple")),
            SimpleTerm("green", "green", _("Green")),
        )
        return SimpleVocabulary(items)
