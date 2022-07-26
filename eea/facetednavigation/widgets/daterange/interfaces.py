""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IDateRangeSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.DateRangeCatalogIndexes",
    )

    calYearRange = schema.TextLine(
        title=_("UI Calendar years range"),
        description=_(
            "Control the range of years"
            "displayed in the year drop-down: "
            "either relative to today's year "
            "(-nn:+nn), relative to the "
            "currently selected year (c-nn:c+nn"
            "), absolute (nnnn:nnnn), or "
            "combinations of these formats "
            "(nnnn:-nn)."
        ),
        required=False,
        default="c-10:c+10",
    )

    usePloneDateFormat = schema.Bool(
        title=_("Reuse date format and language used by Plone"),
        description=_(
            "Reuse the same date format and the "
            "the same language that Plone uses "
            "elsewhere. Otherwise, the format will "
            'be "yy-mm-dd" and the language "English". '
            "Note that this default format allows "
            "you to encode very old or big years "
            "(example : 0001 will not be converted "
            "to 1901). Other formats do not."
        ),
        required=False,
    )

    labelStart = schema.TextLine(
        title=_("Label (start date)"),
        description=_("Text to be displayed as start date input label"),
        required=False,
    )

    labelEnd = schema.TextLine(
        title=_("Label (end date)"),
        description=_("Text to be displayed as end date input label"),
        required=False,
    )

    placeholderStart = schema.TextLine(
        title=_("Placeholder (start date)"),
        description=_("Text to be displayed as start date input placeholder"),
        required=False,
    )

    placeholderEnd = schema.TextLine(
        title=_("Placeholder (end date)"),
        description=_("Text to be displayed as end date input placeholder"),
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IDateRangeSchema).select("title", "index", "default")


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(IDateRangeSchema).select(
        "calYearRange",
        "usePloneDateFormat",
        "labelStart",
        "labelEnd",
        "placeholderStart",
        "placeholderEnd",
    )


__all__ = [
    IDateRangeSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
