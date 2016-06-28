""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _

class IAlphabeticWidget(IWidget):
    """ Alphabetic widget
    """

class IAlphabeticSchema(ISchema):
    """ Schema for Alphabetic Faceted Widget
    """
    default = schema.TextLine(
        title=_(u"Default value"),
        description=_(u"Default letter to be selected"),
        required=False
    )
    default._type = (unicode, str)

    index = schema.Choice(
        title=_(u"Catalog index"),
        description=_(u"Catalog index to use for search"),
        vocabulary=u'eea.faceted.vocabularies.AlphabeticCatalogIndexes'
    )

class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IAlphabeticSchema).select(
        u'title',
        u'default',
        u'index'
    )

__all__ = [
    IAlphabeticSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
]
