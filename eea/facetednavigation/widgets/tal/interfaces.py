""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _
import six


class ITalSchema(ISchema):
    """Widget"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.SortingCatalogIndexes",
    )

    default = schema.TextLine(
        title=_("Tal Expression"),
        description=_("Default tal expression for query value"),
        required=False,
        default="string:",
    )
    default._type = (six.text_type, str)


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(ITalSchema).select(
        "title",
        "index",
        "default",
    )


__all__ = [
    ITalSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
