""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import _


class IDebugSchema(ISchema):
    """Schema"""

    user = schema.Choice(
        title=_("Visible to"),
        description=_("Widget will be visible only for selected user"),
        vocabulary="eea.faceted.vocabularies.CurrentUser",
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IDebugSchema).select(
        "title",
        "default",
        "user",
    )


__all__ = [
    IDebugSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
