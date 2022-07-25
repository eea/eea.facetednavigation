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


class IDateRangeSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u"eea.faceted.vocabularies.DateRangeCatalogIndexes",
    )

    calYearRange = schema.TextLine(
        title=_(u'UI Calendar years range'),
        description=_(u'Control the range of years'
                      u'displayed in the year drop-down: '
                      u'either relative to today\'s year '
                      u'(-nn:+nn), relative to the '
                      u'currently selected year (c-nn:c+nn'
                      u'), absolute (nnnn:nnnn), or '
                      u'combinations of these formats '
                      u'(nnnn:-nn).'),
        required=False,
        default=u"c-10:c+10"
    )
    calYearRange._type = (str, six.text_type)

    usePloneDateFormat = schema.Bool(
        title=_(u'Reuse date format and language used by Plone'),
        description=_(u'Reuse the same date format and the '
                      u'the same language that Plone uses '
                      u'elsewhere. Otherwise, the format will '
                      u'be "yy-mm-dd" and the language "English". '
                      u'Note that this default format allows '
                      u'you to encode very old or big years '
                      u'(example : 0001 will not be converted '
                      u'to 1901). Other formats do not.'),
        required=False
    )

    labelStart = schema.TextLine(
        title=_(u"Label (start date)"),
        description=_(u"Text to be displayed as start date input label"),
        required=False
    )
    labelStart._type = (str, six.text_type)

    labelEnd = schema.TextLine(
        title=_(u"Label (end date)"),
        description=_(u"Text to be displayed as end date input label"),
        required=False
    )
    labelEnd._type = (str, six.text_type)

    placeholderStart = schema.TextLine(
        title=_(u"Placeholder (start date)"),
        description=_(u"Text to be displayed as start date input placeholder"),
        required=False
    )
    placeholderStart._type = (str, six.text_type)

    placeholderEnd = schema.TextLine(
        title=_(u"Placeholder (end date)"),
        description=_(u"Text to be displayed as end date input placeholder"),
        required=False
    )
    placeholderEnd._type = (str, six.text_type)


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IDateRangeSchema).select(
        u'title',
        u'index',
        u'default'
    )


class DisplaySchemata(FacetedSchemata):
    """ Schemata display
    """
    label = u"display"
    fields = field.Fields(IDateRangeSchema).select(
        u'calYearRange',
        u'usePloneDateFormat',
        u'labelStart',
        u'labelEnd',
        u'placeholderStart',
        u'placeholderEnd'
    )


__all__ = [
    IDateRangeSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
