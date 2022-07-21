""" Widget Sections Vocabularies
"""
from eea.facetednavigation.vocabularies.utils import IVocabularyFactory
from eea.facetednavigation.vocabularies import EEAMessageFactory as _
from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm


@implementer(IVocabularyFactory)
class WidgetSections(object):
    """ Widget position in page
    """

    def __call__(self, *args, **kwargs):

        items = (
            SimpleTerm('default', 'default', _('Basic search')),
            SimpleTerm('advanced', 'advanced', _('Extended search')),
        )
        return SimpleVocabulary(items)
