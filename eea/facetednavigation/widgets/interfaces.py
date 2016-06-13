""" Widgets interfaces
"""
from zope import schema
from zope.interface import Interface
from z3c.form import group, field
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import GlobalInterface
from eea.facetednavigation import EEAMessageFactory as _


class ICriterion(Interface):
    """ Model to store search criteria
    """


class IWidget(Interface):
    """ Basic widget
    """


class IWidgetFilterBrains(Interface):
    """ Adapter to filter brains after catalog query.
    """
    def __call__(brains, form):
        """ Filter brains.
        """


class IWidgetsInfo(Interface):
    """ Utility to get available widgets
    """


class IWidgetDirective(Interface):
    """
    Register a widget
    """
    factory = GlobalObject(
        title=_("Factory"),
        description=_("Python name of a factory which can create the"
                      " implementation object.  This must identify an"
                      " object in a module using the full dotted name."),
        required=True,
    )

    schema = GlobalInterface(
        title=_("Schema interface"),
        description=_("An interface describing schema to be used"
                      " within z3c.form"),
        required=False
    )

    accessor = GlobalObject(
        title=_("Accessor"),
        description=_("Accessor to extract data for faceted widget."),
        required=False
    )

    criterion = GlobalInterface(
        title=_("Criterion interface"),
        description=_("Criterion interface"),
        required=False
    )


class ISchema(Interface):
    """ Common edit schema for Faceted Widgets
    """
    title = schema.TextLine(
        title=_(u"Friendly name"),
        description=_(u"Title for widget to display in view page"),
    )
    title._type = (unicode, str)

    default = schema.TextLine(
        title=_(u"Default value"),
        description=_(u"Default query"),
        required=False
    )
    default._type = (unicode, str)

    index = schema.Choice(
        title=_("Catalog index"),
        description=_(u'Catalog index to be used'),
        vocabulary="eea.faceted.vocabularies.CatalogIndexes"
    )

    position = schema.Choice(
        title=_(u'Position'),
        description=_(u"Widget position in page"),
        vocabulary="eea.faceted.vocabularies.WidgetPositions",
        required=False
    )

    section = schema.Choice(
        title=_(u"Section"),
        description=_("Display widget in section"),
        vocabulary="eea.faceted.vocabularies.WidgetSections",
        required=False
    )

    hidden = schema.Bool(
        title=_(u'Hidden'),
        description=_(u"Hide widget"),
        required=False
    )

    count = schema.Bool(
        title=_(u"Count results"),
        description=_(u"Display number of results near each option"),
        required=False
    )

    sortcountable = schema.Bool(
        title=_(u"Sort by countable"),
        description=_(u"Use the results counter for sorting"),
        required=False
    )

    hidezerocount = schema.Bool(
        title=_(u'Hide items with zero results'),
        description=_(u"This option works only if 'count results' is enabled"),
        required=False
    )


class DefaultSchemata(group.Group):
    """ Schemata default
    """
    label = "default"
    fields = field.Fields(ISchema).select(
        'title',
        'default',
        'index'
    )


class LayoutSchemata(group.Group):
    """ Schemata layout
    """
    label = "layout"
    fields = field.Fields(ISchema).select(
        'position',
        'section',
        'hidden'
    )


class CountableSchemata(group.Group):
    """ Schemata countable
    """
    label = "countable"
    fields = field.Fields(ISchema).select(
        'count',
        'sortcountable',
        'hidezerocount'
    )
