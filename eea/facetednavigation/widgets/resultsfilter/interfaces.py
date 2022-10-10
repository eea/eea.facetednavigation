""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IResultsFilterWidget(IWidget):
    """Results Filter widget"""


class IResultsFilterSchema(ISchema):
    """Schema"""

    default = schema.TextLine(
        title=_("Results Filter"),
        description=_("Default tal expression for query value"),
        required=False,
        default='python:hasattr(brain, u"Title")',
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IResultsFilterSchema).select(
        "title",
        "default",
    )


__all__ = [
    IResultsFilterWidget.__name__,
    IResultsFilterSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
