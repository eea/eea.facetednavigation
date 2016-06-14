""" Widget interfaces and schema
"""
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import field, group
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation import EEAMessageFactory as _



class ICheckboxSchema(ISchema):
    """ Schema
    """
    operator = schema.Choice(
        title=_(u'Default operator'),
        description=_(u'Search with AND/OR between elements'),
        vocabulary=SimpleVocabulary([
            SimpleTerm('or', 'or', 'OR'),
            SimpleTerm('and', 'and', 'AND')
        ]),
        default='or'
    )

    operator_visible = schema.Bool(
        title=_(u"Operator visible"),
        description=_(u"Let the end-user choose to search with "
                      u"AND or OR between elements"),
        required=False,
        default=False
    )

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

    maxitems = schema.Int(
        title=_(u"Maximum items"),
        description=_(u'Number of items visible in widget'),
        default=0,
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
    fields = field.Fields(ICheckboxSchema).select(
        'title',
        'index',
        'operator',
        'operator_visible',
        'vocabulary',
        'catalog',
        'default'
    )

class DisplaySchemata(group.Group):
    """ Schemata display
    """
    label = 'display'
    fields = field.Fields(ICheckboxSchema).select(
        'maxitems',
        'sortreversed',
    )


__all__ = [
    ICheckboxSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
]
