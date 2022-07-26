""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class ITextSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.TextCatalogIndexes",
        required=True,
    )

    onlyallelements = schema.Bool(
        title=_("Search in all elements only"),
        description=_(
            "If this checkbox is checked, hides the choice to "
            "filter in all items or in current items only"
        ),
        required=False,
    )

    wildcard = schema.Bool(
        title=_("Wildcard search"),
        description=_(
            "If this checkbox is checked, the system will "
            "automatically do a wildcard search by appending "
            "a '*' to the search term so "
            "searching for 'budget' will also return elements "
            "containing 'budgetary'."
        ),
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(ITextSchema).select(
        "title", "default", "index", "onlyallelements", "wildcard"
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(ITextSchema).select("placeholder")


__all__ = [
    ITextSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
