""" Faceted vocabularies
"""
from zope.interface import implementer
from zope.component.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.vocabularies.utils import lowercase_text


#
# Intersect portal_types with portal_faceted types
#
@implementer(IVocabularyFactory)
class FacetedPortalTypesVocabulary(object):
    """Vocabulary factory for faceted portal types."""

    def __call__(self, *args, **kwargs):
        site = getSite()
        ptool = getToolByName(site, "plone_utils", None)
        ttool = getToolByName(site, "portal_types", None)
        ftool = getToolByName(site, "portal_faceted", None)

        if ptool is None or ttool is None:
            return SimpleVocabulary([])

        items = dict((t, ttool[t].Title()) for t in ptool.getUserFriendlyTypes())

        if ftool is not None:
            faceted_items = dict(
                (t.getId(), t.title_or_id()) for t in ftool.objectValues()
            )
            items.update(faceted_items)

        items = items.items()
        items = sorted(items, key=lowercase_text)

        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)


#
# Get only portal_faceted types
#
@implementer(IVocabularyFactory)
class FacetedOnlyPortalTypesVocabulary(object):
    """Vocabulary factory only for faceted portal types."""

    def __call__(self, *args, **kwargs):
        ftool = getToolByName(getSite(), "portal_faceted", None)

        if ftool is None:
            return SimpleVocabulary([])

        items = dict((t.getId(), t.title_or_id()) for t in ftool.objectValues())

        items = items.items()
        items.sort(key=lowercase_text)

        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)
