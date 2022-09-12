""" Widget interfaces and schema
"""
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema, FacetedSchemata
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation import _


class IMultiSelectSchema(ISchema):
    """Schema"""

    default = schema.List(
        title=_("Default value"),
        description=_("Default items (one per line)"),
        required=False,
        unique=True,
        value_type=schema.TextLine(title="Item"),
    )

    operator = schema.Choice(
        title=_("Default operator"),
        description=_("Search with AND/OR between elements"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm("or", "or", "OR"), SimpleTerm("and", "and", "AND")]
        ),
        default="or",
    )

    operator_visible = schema.Bool(
        title=_("Operator visible"),
        description=_(
            "Let the end-user choose to search with " "AND or OR between elements"
        ),
        required=False,
        default=False,
    )

    multiple = schema.Bool(
        title=_("Multiselect"),
        description=_("Allow multiple selections"),
        default=True,
        required=False,
    )

    vocabulary = schema.Choice(
        title=_("Vocabulary"),
        description=_("Vocabulary to use to render widget items"),
        vocabulary="eea.faceted.vocabularies.PortalVocabularies",
        required=False,
    )

    ajax = schema.TextLine(
        title=_("AJAX URL"),
        description=_(
            "Provide an URL to be used to get and filter items "
            "asynchronously e.g.: /search. Your endpoint should "
            "filter items by 'q' param and return a JSON like "
            "e.g.: {'items': [...]}"
        ),
        required=False,
    )

    catalog = schema.Choice(
        title=_("Catalog"),
        description=_(
            "Get unique values from catalog " "as an alternative for vocabulary"
        ),
        vocabulary="eea.faceted.vocabularies.UseCatalog",
        required=False,
    )

    closeonselect = schema.Bool(
        title=_("Close on select"),
        description=_("Close selection popup after each select"),
        required=False,
    )

    sortreversed = schema.Bool(
        title=_("Reverse options"),
        description=_("Sort options reversed"),
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IMultiSelectSchema).select(
        "title",
        "index",
        "operator",
        "operator_visible",
        "multiple",
        "vocabulary",
        "catalog",
        "ajax",
        "default",
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(IMultiSelectSchema).select(
        "sortreversed", "closeonselect", "placeholder"
    )


__all__ = [
    IMultiSelectSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
]
