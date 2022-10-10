""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IAlphabeticWidget(IWidget):
    """Alphabetic widget"""


class IAlphabeticSchema(ISchema):
    """Schema for Alphabetic Faceted Widget"""

    default = schema.TextLine(
        title=_("Default value"),
        description=_("Default letter to be selected"),
        required=False,
    )

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.AlphabeticCatalogIndexes",
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IAlphabeticSchema).select("title", "default", "index")


__all__ = [
    IAlphabeticSchema.__name__,
    DefaultSchemata.__name__,
    CountableSchemata.__name__,
    LayoutSchemata.__name__,
]
