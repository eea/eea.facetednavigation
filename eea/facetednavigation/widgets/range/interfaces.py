""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class IRangeSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u"eea.faceted.vocabularies.RangeCatalogIndexes",
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IRangeSchema).select(
        u'title',
        u'default',
        u'index',
    )


__all__ = [
    IRangeSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
