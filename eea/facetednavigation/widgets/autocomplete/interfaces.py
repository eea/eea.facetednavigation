""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.plonex import ISolrConnectionManager
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class IAutocompleteSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u"eea.faceted.vocabularies.TextCatalogIndexes",
    )

    autocomplete_view = schema.Choice(
        title=_(u"Autocomplete"),
        description=_(u'Select the source of the autocomplete suggestions'),
        vocabulary=u'eea.faceted.vocabularies.AutocompleteViews',
    )

    onlyallelements = schema.Bool(
        title=_(u'Search in all elements only'),
        description=_(u'If this checkbox is checked, hides the choice to '
                      u'filter in all items or in current items only'),
        required=False
    )

    multivalued = schema.Bool(
        title=_(u'Can select several elements'),
        description=_(u"Can select multiple values"),
        required=False
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IAutocompleteSchema).select(
        u'title',
        u'default',
        u'index',
        u'autocomplete_view',
        u'onlyallelements',
        u'multivalued'
    )


__all__ = [
    ISolrConnectionManager.__name__,
    IAutocompleteSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
