""" Catalog specific vocabularies
"""
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer
from zope.component.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.vocabularies.utils import lowercase_text


#
# Object provides
#
@implementer(IVocabularyFactory)
class ObjectProvidesVocabulary(object):
    """Vocabulary factory for object provides index."""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        if not ctool:
            return SimpleVocabulary([])

        provides = ctool.Indexes.get("object_provides", None)
        if not provides:
            return SimpleVocabulary([])

        items = list(provides.uniqueValues())
        items.sort(key=str.lower)
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)


#
# Catalog indexes
#
@implementer(IVocabularyFactory)
class CatalogIndexesVocabulary(object):
    """Return catalog indexes as vocabulary"""

    def _labels(self):
        """Get indexes labels from portal_atct settings"""
        registry = getUtility(IRegistry)
        config = IQuerystringRegistryReader(registry)()
        indexes = config.get("indexes", {})

        res = {}
        for index, ob in indexes.items():
            res[index] = ob.get("title", index)
        return res

    def _create_vocabulary(self, indexes):
        """Create voc"""
        labels = self._labels()
        res = [(term, labels.get(term, "") or term) for term in indexes]
        res.sort(key=lowercase_text)
        res.insert(0, ("", ""))
        items = [SimpleTerm(key, key, value) for key, value in res]
        return SimpleVocabulary(items)

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        indexes = ctool.Indexes.keys()
        return self._create_vocabulary(indexes)


#
# Rangeable catalog indexes
#
@implementer(IVocabularyFactory)
class RangeCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """Filter catalog indexes for alphabetic widget"""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        res = []
        for index in ctool.getIndexObjects():
            index_id = index.getId()
            if index.meta_type in ("FieldIndex",):
                res.append(index_id)

        return self._create_vocabulary(res)


#
# Alphabetic catalog indexes
#
@implementer(IVocabularyFactory)
class AlphabeticCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """Filter catalog indexes for alphabetic widget"""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        schema = ctool.schema()
        res = []
        for index in ctool.getIndexObjects():
            index_id = index.getId()
            if index_id not in schema:
                continue
            elif index.meta_type not in ("FieldIndex", "TextIndex", "ZCTextIndex"):
                continue
            else:
                res.append(index_id)

        return self._create_vocabulary(res)


#
# Date range catalog indexes
#
@implementer(IVocabularyFactory)
class DateRangeCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """Filter catalog indexes for daterange widget"""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        res = []
        for index in ctool.getIndexObjects():
            index_id = index.getId()
            if index.meta_type in ("DateIndex", "DateRecurringIndex"):
                res.append(index_id)

        return self._create_vocabulary(res)


#
# Text catalog indexes
#
class TextCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """Filter catalog indexes for text widget"""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        res = []
        for index in ctool.getIndexObjects():
            index_id = index.getId()
            if index.meta_type not in ("DateIndex", "DateRangeIndex"):
                res.append(index_id)

        return self._create_vocabulary(res)


#
# Path catalog indexes
#
class PathCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """Filter catalog indexes for path widget"""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        res = []
        for index in ctool.getIndexObjects():
            index_id = index.getId()
            if index.meta_type in ("PathIndex", "ExtendedPathIndex"):
                res.append(index_id)

        return self._create_vocabulary(res)


#
# Simple fields catalog indexes
# Mono valued indexes
#
class SimpleFieldCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """Filter catalog indexes for simple fields"""

    def __call__(self, *args, **kwargs):
        """See IVocabularyFactory interface"""
        ctool = getToolByName(getSite(), "portal_catalog")
        res = []
        for index in ctool.getIndexObjects():
            index_id = index.getId()
            if index.meta_type in ("FieldIndex", "BooleanIndex"):
                res.append(index_id)

        return self._create_vocabulary(res)


#
# Sorting catalog indexes
#
class SortingCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """Also include sort_on and sort_order indexes"""

    def __call__(self, *args, **kwargs):
        voc = super(SortingCatalogIndexesVocabulary, self).__call__()
        terms = voc._terms
        terms.extend(
            (
                SimpleTerm("sort_on", "sort_on", "Sort On"),
                SimpleTerm("sort_order", "sort_order", "Sort Order"),
            )
        )
        return SimpleVocabulary(terms)
