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


class ISelectSchema(ISchema):
    """Schema"""

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

    hidealloption = schema.Bool(
        title=_("Hide 'All' option"),
        description=_('If this checkbox is checked, hides the "All" option'),
        required=False,
    )

    sortreversed = schema.Bool(
        title=_("Reverse options"),
        description=_("Sort options reversed"),
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(ISelectSchema).select(
        "title", "index", "vocabulary", "catalog", "hidealloption", "default"
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(ISelectSchema).select(
        "sortreversed",
    )


__all__ = [
    ISelectSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
]
