""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata as LS
from z3c.form import field
from zope import schema


class IETagSchema(ISchema):
    """Schema"""

    hidden = schema.Bool(
        title=_("Enabled (hidden)"),
        description=_("Hide this widget in order for e-tag to be used"),
        required=False,
        default=True,
    )

    default = schema.TextLine(
        title=_("Default value"),
        description=_("Default e-tag"),
        required=False,
        default="1.0",
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IETagSchema).select(
        "title",
        "default",
        "hidden",
    )


class LayoutSchemata(LS):
    """Schemata default"""

    fields = field.Fields(IETagSchema).select(
        "position",
        "section",
    )


__all__ = [
    IETagSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
