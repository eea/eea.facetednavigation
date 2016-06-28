""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class IPortletSchema(ISchema):
    """ Schema
    """
    macro = schema.TextLine(
        title=_(u'Portlet macro'),
        description=_(u'Path to portlet macro'),
    )
    macro._type = (unicode, str)


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IPortletSchema).select(
        u'title',
        u'default',
        u'macro',
    )

__all__ = [
    IPortletSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
