""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import CountableSchemata as CS
from eea.facetednavigation import EEAMessageFactory as _


class IBooleanSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u"eea.faceted.vocabularies.SimpleFieldCatalogIndexes",
        required=True
    )

    default = schema.Bool(
        title=_(u'Default value'),
        description=_(u'Default value'),
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IBooleanSchema).select(
        u'title',
        u'default',
        u'index',
    )


class CountableSchemata(CS):
    """ Schemata countable
    """
    fields = field.Fields(ISchema).select(
        u'count'
    )


__all__ = [
    IBooleanSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
