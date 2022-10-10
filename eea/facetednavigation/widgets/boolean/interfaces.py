""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import CountableSchemata as CS
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IBooleanSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.SimpleFieldCatalogIndexes",
        required=True,
    )

    default = schema.Bool(
        title=_("Default value"),
        description=_("Default value"),
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IBooleanSchema).select(
        "title",
        "default",
        "index",
    )


class CountableSchemata(CS):
    """Schemata countable"""

    fields = field.Fields(ISchema).select("count")


__all__ = [
    IBooleanSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
