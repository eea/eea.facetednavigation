""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class IDebugSchema(ISchema):
    """ Schema
    """
    user = schema.Choice(
        title=_(u'Visible to'),
        description=_(u'Widget will be visible only for selected user'),
        vocabulary=u'eea.faceted.vocabularies.CurrentUser',
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IDebugSchema).select(
        u'title',
        u'default',
        u'user',
    )

__all__ = [
    IDebugSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
