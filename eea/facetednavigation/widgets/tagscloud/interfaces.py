""" Widget interfaces and schema
"""
from eea.facetednavigation import _
from eea.facetednavigation.widgets.interfaces import CountableSchemata
from eea.facetednavigation.widgets.interfaces import DefaultSchemata as DS
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from eea.facetednavigation.widgets.interfaces import ISchema
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from z3c.form import field
from zope import schema
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


TagsCloudVocabulary = SimpleVocabulary(
    [
        SimpleTerm("list", "list", _("List")),
        SimpleTerm("sphere", "sphere", _("Sphere")),
        SimpleTerm("cloud", "cloud", _("Cloud")),
    ]
)


class ITagsCloudSchema(ISchema):
    """Schema"""

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to use for search"),
        vocabulary="eea.faceted.vocabularies.CatalogIndexes",
    )

    vocabulary = schema.Choice(
        title=_("Vocabulary"),
        description=_("Vocabulary to use to render widget items"),
        vocabulary="eea.faceted.vocabularies.PortalVocabularies",
        required=False,
    )

    catalog = schema.Choice(
        title=_("Catalog"),
        description=_(
            "Get unique values from catalog " "as an alternative for vocabulary"
        ),
        vocabulary="eea.faceted.vocabularies.UseCatalog",
        required=False,
    )

    hidealloption = schema.Bool(
        title=_("Hide 'All' option"),
        description=_('If this checkbox is checked, hides the "All" option'),
        required=False,
    )

    maxitems = schema.Int(
        title=_("Maximum items"),
        description=_("Number of items visible in widget"),
        default=50,
        required=False,
    )

    maxchars = schema.Int(
        title=_("Maximum characters"),
        description=_("Cut long phrases to provided number of characters"),
        default=0,
        required=False,
    )

    sortreversed = schema.Bool(
        title=_("Reverse options"),
        description=_("Sort options reversed"),
        required=False,
    )

    colormin = schema.TextLine(
        title=_("Minimum color"),
        description=_("Tagscloud minimum color"),
        default="9acee6",
        required=False,
    )

    colormax = schema.TextLine(
        title=_("Maximum color"),
        description=_("Tagscloud max color"),
        default="007bb3",
        required=False,
    )

    cloud = schema.Choice(
        title=_("Cloud type"),
        description=_("Type of the cloud"),
        vocabulary=TagsCloudVocabulary,
    )

    sizemin = schema.Int(
        title=_("Minimum size"),
        description=_("Minimum font-size (px)"),
        required=False,
        default=10,
    )

    sizemax = schema.Int(
        title=_("Maximum size"),
        description=_("Maximum font-size (px)"),
        required=False,
        default=20,
    )

    height = schema.Int(
        title=_("Cloud height"),
        description=_("Cloud height (px)"),
        required=False,
        default=200,
    )


class DefaultSchemata(DS):
    """Schemata default"""

    fields = field.Fields(ITagsCloudSchema).select(
        "title", "index", "vocabulary", "catalog", "default"
    )


class DisplaySchemata(FacetedSchemata):
    """Schemata display"""

    label = "display"
    fields = field.Fields(ITagsCloudSchema).select(
        "maxitems",
        "maxchars",
        "colormin",
        "colormax",
        "sortreversed",
    )


class GeometrySchemata(FacetedSchemata):
    """Schemata geometry"""

    label = "geometry"
    fields = field.Fields(ITagsCloudSchema).select(
        "cloud", "sizemin", "sizemax", "height"
    )


__all__ = [
    ITagsCloudSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
    GeometrySchemata.__name__,
]
