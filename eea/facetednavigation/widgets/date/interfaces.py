""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class IDateSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.DateRangeCatalogIndexes",
        required=True,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IDateSchema).select(
        "title",
        "default",
        "index",
    )


__all__ = [
    IDateSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
