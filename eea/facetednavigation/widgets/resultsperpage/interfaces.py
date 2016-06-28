""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema, FacetedSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class IResultsPerPageSchema(ISchema):
    """ Schema
    """
    start = schema.Int(
        title=_(u'Start'),
        description=_(u'Results per page starting value'),
        required=False,
        default=0
    )

    end = schema.Int(
        title=_(u'End'),
        description=_(u'Results per page ending value'),
        required=False,
        default=50
    )

    step = schema.Int(
        title=_(u'Step'),
        description=_(u'Results per page step'),
        required=False,
        default=5
    )

    default = schema.Int(
        title=_(u'Default value'),
        description=_(u'Default results per page'),
        required=False,
        default=20
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IResultsPerPageSchema).select(
        u'title',
        u'default',
    )


class DisplaySchemata(FacetedSchemata):
    """ Schemata display
    """
    label = u'display'
    fields = field.Fields(IResultsPerPageSchema).select(
        u'start',
        u'end',
        u'step'
    )


__all__ = [
    IResultsPerPageSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
