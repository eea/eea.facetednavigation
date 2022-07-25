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
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u"eea.faceted.vocabularies.RangeCatalogIndexes",
    )

    labelStart = schema.TextLine(
        title=_(u"Label (start range)"),
        description=_(u"Text to be displayed as start range input label"),
        required=False
    )
    labelStart._type = (str, six.text_type)

    labelEnd = schema.TextLine(
        title=_(u"Label (end range)"),
        description=_(u"Text to be displayed as end range input label"),
        required=False
    )
    labelEnd._type = (str, six.text_type)

    placeholderStart = schema.TextLine(
        title=_(u"Placeholder (start range)"),
        description=_(u"Text to be displayed as start range input placeholder"),
        required=False
    )
    placeholderStart._type = (str, six.text_type)

    placeholderEnd = schema.TextLine(
        title=_(u"Placeholder (end range)"),
        description=_(u"Text to be displayed as end range input placeholder"),
        required=False
    )
    placeholderEnd._type = (str, six.text_type)

    integer = schema.Bool(
        title=_(u"Numerical range"),
        description=_(u"Allow to input only numerical digits"),
        required=False,
        default=False
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IRangeSchema).select(
        u'title',
        u'default',
        u'index',
        u'integer',
    )

class DisplaySchemata(FacetedSchemata):
    """ Schemata display
    """
    label = u"display"
    fields = field.Fields(IRangeSchema).select(
        u'labelStart',
        u'labelEnd',
        u'placeholderStart',
        u'placeholderEnd'
    )

__all__ = [
    IRangeSchema.__name__,
    DefaultSchemata.__name__,
    DisplaySchemata.__name__,
    LayoutSchemata.__name__,
]
