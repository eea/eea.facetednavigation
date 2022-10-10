""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class ISortingSchema(ISchema):
    """Schema"""

    vocabulary = schema.Choice(
        title=_("Filter from vocabulary"),
        description=_(
            "Vocabulary to use to filter sorting criteria. "
            "Leave empty for default sorting criteria."
        ),
        vocabulary="eea.faceted.vocabularies.PortalVocabularies",
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(ISortingSchema).select("title", "vocabulary", "default")


__all__ = [
    ISortingSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
