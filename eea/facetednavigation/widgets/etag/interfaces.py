""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata as LS
from eea.facetednavigation import EEAMessageFactory as _


class IETagSchema(ISchema):
    """ Schema
    """
    hidden = schema.Bool(
        title=_(u'Enabled (hidden)'),
        description=_(u"Hide this widget in order for e-tag to be used"),
        required=False,
        default=True
    )

    default = schema.TextLine(
        title=_(u"Default value"),
        description=_(u"Default e-tag"),
        required=False,
        default=u"1.0"
    )
    default._type = (unicode, str)


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IETagSchema).select(
        u'title',
        u'default',
        u'hidden',
    )


class LayoutSchemata(LS):
    """ Schemata default
    """
    fields = field.Fields(IETagSchema).select(
        u'position',
        u'section',
    )


__all__ = [
    IETagSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
