""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.plonex import ISolrConnectionManager
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IAutocompleteSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.TextCatalogIndexes",
    )

    autocomplete_view = schema.Choice(
        title=_("Autocomplete"),
        description=_("Select the source of the autocomplete suggestions"),
        vocabulary="eea.faceted.vocabularies.AutocompleteViews",
    )

    onlyallelements = schema.Bool(
        title=_("Search in all elements only"),
        description=_(
            "If this checkbox is checked, hides the choice to "
            "filter in all items or in current items only"
        ),
        required=False,
    )

    multivalued = schema.Bool(
        title=_("Can select several elements"),
        description=_("Can select multiple values"),
        required=False,
    )

    hidebutton = schema.Bool(
        title=_("Hide search button"),
        description=_("Do not display the search button"),
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IAutocompleteSchema).select(
        "title",
        "default",
        "index",
        "autocomplete_view",
        "onlyallelements",
        "multivalued",
        "hidebutton",
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(IAutocompleteSchema).select("placeholder")


__all__ = [
    ISolrConnectionManager.__name__,
    IAutocompleteSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
