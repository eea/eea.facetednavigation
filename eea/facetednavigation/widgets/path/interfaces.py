""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema


class IPathSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.PathCatalogIndexes",
        required=True,
        default="path",
    )

    root = schema.TextLine(
        title=_("Root folder"),
        description=_(
            "Navigation js-tree starting point "
            "(relative to plone site. ex: SITE/data-and-maps)"
        ),
        required=False,
    )

    depth = schema.TextLine(
        title=_("Search Depth"),
        description=_(
            "Depth to search the path. 0=this level, "
            "-1=all subfolders recursive, and any other positive "
            "integer count the subfolder-levels to search."
        ),
        required=False,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(IPathSchema).select(
        "title",
        "default",
        "index",
        "root",
        "depth",
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(IPathSchema).select("placeholder")


__all__ = [
    IPathSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    DisplaySchemata.__name__,
]
