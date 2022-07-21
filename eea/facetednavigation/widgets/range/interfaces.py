""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _

import six


class IRangeSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.RangeCatalogIndexes",
    )

    labelStart = schema.TextLine(
        title=_("Label (start range)"),
        description=_("Text to be displayed as start range input label"),
        required=False,
    )
    labelStart._type = (str, six.text_type)

    labelEnd = schema.TextLine(
        title=_("Label (end range)"),
        description=_("Text to be displayed as end range input label"),
        required=False,
    )
    labelEnd._type = (str, six.text_type)

    placeholderStart = schema.TextLine(
        title=_("Placeholder (start range)"),
        description=_("Text to be displayed as start range input placeholder"),
        required=False,
    )
    placeholderStart._type = (str, six.text_type)

    placeholderEnd = schema.TextLine(
        title=_("Placeholder (end range)"),
        description=_("Text to be displayed as end range input placeholder"),
        required=False,
    )
    placeholderEnd._type = (str, six.text_type)

    integer = schema.Bool(
        title=_("Numerical range"),
        description=_("Allow to input only numerical digits"),
        required=False,
        default=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IRangeSchema).select(
        "title",
        "default",
        "index",
        "integer",
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(IRangeSchema).select(
        "labelStart", "labelEnd", "placeholderStart", "placeholderEnd"
    )


__all__ = [
    IRangeSchema.__name__,
    DefaultSchemata.__name__,
    DisplaySchemata.__name__,
    LayoutSchemata.__name__,
]
