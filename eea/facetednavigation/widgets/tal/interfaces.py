""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class ITalSchema(ISchema):
    """ Widget
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u'eea.faceted.vocabularies.SortingCatalogIndexes'
    )

    default = schema.TextLine(
        title=_(u'Tal Expression'),
        description=_(u'Default tal expression for query value'),
        required=False,
        default=u'string:',
    )
    default._type = (unicode, str)


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(ITalSchema).select(
        u'title',
        u'index',
        u'default',
    )


__all__ = [
    ITalSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
