""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IPortletSchema(ISchema):
    """Schema"""

    macro = schema.TextLine(
        title=_("Portlet macro"),
        description=_("Path to portlet macro"),
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IPortletSchema).select(
        "title",
        "default",
        "macro",
    )


__all__ = [
    IPortletSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
