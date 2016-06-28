""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class ICriteriaSchema(ISchema):
    """ Schema
    """
    hidecriteriaenabled = schema.Bool(
        title=_(u'Enable hide/show criteria'),
        description=_(u"Uncheck this box if you don't want hide/show "
                      u"criteria feature enabled on this widget"),
        required=False,
        default=True
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(ICriteriaSchema).select(
        u'title',
        u'hidecriteriaenabled'
    )


__all__ = [
    ICriteriaSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
