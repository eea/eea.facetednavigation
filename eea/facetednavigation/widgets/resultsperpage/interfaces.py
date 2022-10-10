""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IResultsPerPageSchema(ISchema):
    """Schema"""

    start = schema.Int(
        title=_("Start"),
        description=_("Results per page starting value"),
        required=False,
        default=0,
    )

    end = schema.Int(
        title=_("End"),
        description=_("Results per page ending value"),
        required=False,
        default=50,
    )

    step = schema.Int(
        title=_("Step"),
        description=_("Results per page step"),
        required=False,
        default=5,
    )

    default = schema.Int(
        title=_("Default value"),
        description=_("Default results per page"),
        required=False,
        default=20,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IResultsPerPageSchema).select(
        "title",
        "default",
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(IResultsPerPageSchema).select("start", "end", "step")


__all__ = [
    IResultsPerPageSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
