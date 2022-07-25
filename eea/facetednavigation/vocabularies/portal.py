""" Portal tools specific vocabularies
"""
from eea.facetednavigation.vocabularies.utils import lowercase_text
from zope.component import getUtilitiesFor
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName

import six


#
# portal_vocabularies
#
@implementer(IVocabularyFactory)
class PortalVocabulariesVocabulary(object):
    """ Return vocabularies in portal_vocabulary
    """

    def __call__(self, *args, **kwargs):
        """ See IVocabularyFactory interface
        """
        res = []
        vtool = getToolByName(getSite(), 'portal_vocabularies', None)
        if vtool:
            vocabularies = vtool.objectValues()
            res.extend([(term.getId(), term.title_or_id())
                        for term in vocabularies])
        atvocabulary_ids = [elem[0] for elem in res]

        factories = getUtilitiesFor(IVocabularyFactory)
        res.extend([(factory[0], factory[0]) for factory in factories
                    if factory[0] not in atvocabulary_ids])

        res.sort(key=lowercase_text)
        # play nice with collective.solr I18NFacetTitlesVocabularyFactory
        # and probably others
        if res and res[0] != ('', ''):
            res.insert(0, ('', ''))
        items = []
        for key, value in res:
            term = SimpleTerm(key, key, value)
            if term not in items:
                items.append(term)
        return SimpleVocabulary(items)


#
# portal_languages
#
@implementer(IVocabularyFactory)
class PortalLanguagesVocabulary(object):
    """ Return portal types as vocabulary
    """

    def __call__(self, *args, **kwargs):
        """ See IVocabularyFactory interface
        """
        portal_languages = getToolByName(getSite(), 'portal_languages', None)
        if not portal_languages:
            return SimpleVocabulary([])

        res = portal_languages.listSupportedLanguages()
        res = [(x, (isinstance(y, six.binary_type) and y.decode('utf-8') or y))
               for x, y in res]

        res.sort(key=lowercase_text)
        items = [SimpleTerm(key, key, value) for key, value in res]
        return SimpleVocabulary(items)
