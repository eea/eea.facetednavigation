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

TagsCloudVocabulary = SimpleVocabulary([
    SimpleTerm(u'list', u'list', _("List")),
    SimpleTerm(u'sphere', u'sphere', _("Sphere")),
    SimpleTerm(u'cloud', u'cloud', _("Cloud"))
])


class ITagsCloudSchema(ISchema):
    """ Schema
    """
    index = schema.Choice(
        title=_(u'Catalog index'),
        description=_(u'Catalog index to use for search'),
        vocabulary="eea.faceted.vocabularies.CatalogIndexes",
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

    hidealloption = schema.Bool(
        title=_(u"Hide 'All' option"),
        description=_(u'If this checkbox is checked, hides the "All" option'),
        required=False
    )

    maxitems = schema.Int(
        title=_(u"Maximum items"),
        description=_(u'Number of items visible in widget'),
        default=50,
        required=False
    )

    maxchars = schema.Int(
        title=_(u'Maximum characters'),
        description=_(u'Cut long phrases to provided number of characters'),
        default=0,
        required=False
    )

    sortreversed = schema.Bool(
        title=_(u"Reverse options"),
        description=_(u"Sort options reversed"),
        required=False
    )

    colormin = schema.TextLine(
        title=_(u'Minimum color'),
        description=_(u'Tagscloud minimum color'),
        default=u"A1BE7E",
        required=False
    )
    colormin._type = (unicode, str)

    colormax = schema.TextLine(
        title=_(u'Maximum color'),
        description=_(u'Tagscloud max color'),
        default=u"95B229",
        required=False
    )
    colormax._type = (unicode, str)

    cloud = schema.Choice(
        title=_('Cloud type'),
        description=_(u'Type of the cloud'),
        vocabulary=TagsCloudVocabulary
    )

    sizemin = schema.Int(
        title=_(u'Minimum size'),
        description=_(u'Minimum font-size (px)'),
        required=False,
        default=10
    )

    sizemax = schema.Int(
        title=_(u'Maximum size'),
        description=_(u'Maximum font-size (px)'),
        required=False,
        default=20
    )

    height = schema.Int(
        title=_(u'Cloud height'),
        description=_(u'Cloud height (px)'),
        required=False,
        default=200
    )


class DefaultSchemata(DS):
    """ Schemata default
    """
    fields = field.Fields(ITagsCloudSchema).select(
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
    fields = field.Fields(ITagsCloudSchema).select(
        'maxitems',
        'maxchars',
        'colormin',
        'colormax',
        'sortreversed',
    )


class GeometrySchemata(group.Group):
    """ Schemata geometry
    """
    label = 'geometry'
    fields = field.Fields(ITagsCloudSchema).select(
        'cloud',
        'sizemin',
        'sizemax',
        'height'
    )


__all__ = [
    ITagsCloudSchema.__name__,
    DefaultSchemata.__name__,
    LayoutSchemata.__name__,
    CountableSchemata.__name__,
    DisplaySchemata.__name__,
    GeometrySchemata.__name__,
]
