""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation import EEAMessageFactory as _


class IRadioSchema(ISchema):
    """ Schema
    """
    vocabulary = schema.Choice(
        title=_(u"Vocabulary"),
        description=_(u'Vocabulary to use to render widget items'),
        vocabulary=u'eea.faceted.vocabularies.PortalVocabularies',
        required=False
    )

    catalog = schema.Choice(
        title=_(u'Catalog'),
        description=_(u"Get unique values from catalog "
                      u"as an alternative for vocabulary"),
        vocabulary=u'eea.faceted.vocabularies.UseCatalog',
        required=False
    )

    hidealloption = schema.Bool(
        title=_(u"Hide 'All' option"),
        description=_(u'If this checkbox is checked, hides the "All" option'),
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
    fields = field.Fields(IRadioSchema).select(
        u'title',
        u'index',
        u'vocabulary',
        u'catalog',
        u'hidealloption',
        u'default'
    )


class DisplaySchemata(FacetedSchemata):
    """ Schemata display
    """
    label = u'display'
    fields = field.Fields(IRadioSchema).select(
        u'maxitems',
        u'sortreversed',
    )


__all__ = [
    IRadioSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
]
