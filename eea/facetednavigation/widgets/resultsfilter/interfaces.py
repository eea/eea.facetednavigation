""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.interfaces import IWidget
from eea.facetednavigation import EEAMessageFactory as _


class IResultsFilterWidget(IWidget):
    """ Results Filter widget
    """


class IResultsFilterSchema(ISchema):
    """ Schema
    """
    default = schema.TextLine(
        title=_(u'Results Filter'),
        description=_(u'Default tal expression for query value'),
        required=False,
        default=u'python:hasattr(brain, u"Title")',
    )
    default._type = (unicode, str)


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IResultsFilterSchema).select(
        u'title',
        u'default',
    )


__all__ = [
    IResultsFilterWidget.__name__,
    IResultsFilterSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
