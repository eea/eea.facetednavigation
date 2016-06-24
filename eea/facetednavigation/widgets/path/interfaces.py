""" Widget interfaces and schema
"""
from zope import schema
from z3c.form import field
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _


class IPathSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary=u"eea.faceted.vocabularies.PathCatalogIndexes",
        required=True,
        default=u'path',
    )

    root = schema.TextLine(
        title=_(u'Root folder'),
        description=_(u'Navigation js-tree starting point '
                      u'(relative to plone site. ex: SITE/data-and-maps)'),
        required=False
    )
    root._type = (unicode, str)

    depth = schema.TextLine(
        title=_(u'Search Depth'),
        description=_(u'Depth to search the path. 0=this level, '
                      u'-1=all subfolders recursive, and any other positive '
                      u'integer count the subfolder-levels to search.'),
        required=False
    )
    depth._type = (unicode, str)

    theme = schema.Choice(
        title=_(u'Navigation tree theme'),
        description=_(u'Theme to be used with this widget'),
        vocabulary=u'eea.faceted.vocabularies.JsTreeThemes',
        default=u'green',
        required=False
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(IPathSchema).select(
        u'title',
        u'default',
        u'index',
        u'root',
        u'depth',
    )


class DisplaySchemata(FacetedSchemata):
    """ Schemata display
    """
    label = u'display'
    fields = field.Fields(IPathSchema).select(
        u'theme'
    )

__all__ = [
    IPathSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
