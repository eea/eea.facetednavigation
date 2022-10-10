""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ICheckboxSchema(ISchema):
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

    vocabulary = schema.Choice(
        title=_("Vocabulary"),
        description=_("Vocabulary to use to render widget items"),
        vocabulary="eea.faceted.vocabularies.PortalVocabularies",
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

    maxitems = schema.Int(
        title=_("Maximum items"),
        description=_("Number of items visible in widget"),
        default=0,
        required=False,
    )

    sortreversed = schema.Bool(
        title=_("Reverse options"),
        description=_("Sort options reversed"),
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(ICheckboxSchema).select(
        "title",
        "index",
        "operator",
        "operator_visible",
        "vocabulary",
        "catalog",
        "default",
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(ICheckboxSchema).select(
        "maxitems",
        "sortreversed",
    )


__all__ = [
    ICheckboxSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
]
