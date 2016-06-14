""" Widget interfaces and schema
"""
from zope.interface import Interface
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _

try:
    from collective.solr import interfaces
    ISolrConnectionManager = interfaces.ISolrConnectionManager
except ImportError:
    class ISolrConnectionManager(Interface):
        """ collective.solr not installed
        """

class IAutocompleteSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary="eea.faceted.vocabularies.TextCatalogIndexes",
    )

    autocomplete_view = schema.Choice(
        title=_(u"Autocomplete"),
        description=_(u'Select the source of the autocomplete suggestions'),
        vocabulary='eea.faceted.vocabularies.AutocompleteViews',
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
        'title',
        'default',
        'index',
        'autocomplete_view',
        'onlyallelements',
        'multivalued'
    )


__all__ = [
    IAutocompleteSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
