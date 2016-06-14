""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field, group
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation import EEAMessageFactory as _


class ISelectSchema(ISchema):
    """ Schema
    """
    vocabulary = schema.Choice(
        title=_(u"Vocabulary"),
        description=_(u'Vocabulary to use to render widget items'),
        vocabulary='eea.faceted.vocabularies.PortalVocabularies',
        required=False
    )

    catalog = schema.Choice(
        title=_(u'Catalog'),
        description=_(u"Get unique values from catalog "
                      u"as an alternative for vocabulary"),
        vocabulary='eea.faceted.vocabularies.UseCatalog',
        required=False
    )

    sortreversed = schema.Bool(
        title=_(u"Reverse options"),
        description=_(u"Sort options reversed"),
        required=False
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(ISelectSchema).select(
        'title',
        'index',
        'vocabulary',
        'catalog',
        'default'
    )


class DisplaySchemata(group.Group):
    """ Schemata display
    """
    label = 'display'
    fields = field.Fields(ISelectSchema).select(
        'sortreversed',
    )


__all__ = [
    ISelectSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
]
