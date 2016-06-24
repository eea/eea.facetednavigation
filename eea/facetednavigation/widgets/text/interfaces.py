""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class ITextSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u"eea.faceted.vocabularies.TextCatalogIndexes",
        required=True
    )

    onlyallelements = schema.Bool(
        title=_(u"Search in all elements only"),
        description=_(u'If this checkbox is checked, hides the choice to '
                      u'filter in all items or in current items only'),
        required=False
    )

    wildcard = schema.Bool(
            title=_(u'Wildcard search'),
            description=_(u"If this checkbox is checked, the system will "
                          u"automatically do a wildcard search by appending "
                          u"a '*' to the search term so "
                          u"searching for 'budget' will also return elements "
                          u"containing 'budgetary'."),
        required=False
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(ITextSchema).select(
        u'title',
        u'default',
        u'index',
        u'onlyallelements',
        u'wildcard'
    )


__all__ = [
    ITextSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
