""" Widgets interfaces
"""
from eea.facetednavigation import _
from z3c.form import field
from z3c.form import group
from zope import schema
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.interface import Interface


class ICriterion(Interface):
    """Model to store search criteria"""


class IWidget(Interface):
    """Basic widget"""


class IWidgetFilterBrains(Interface):
    """Adapter to filter brains after catalog query."""

    def __call__(brains, form):
        """Filter brains."""


class IWidgetsInfo(Interface):
    """Utility to get available widgets"""


class IWidgetDirective(Interface):
    """
    Register a widget
    """

    factory = GlobalObject(
        title=_("Factory"),
        description=_(
            "Python name of a factory which can create the"
            " implementation object.  This must identify an"
            " object in a module using the full dotted name."
        ),
        required=True,
    )

    schema = GlobalInterface(
        title=_("Schema interface"),
        description=_("An interface describing schema to be used" " within z3c.form"),
        required=False,
    )

    accessor = GlobalObject(
        title=_("Accessor"),
        description=_("Accessor to extract data for faceted widget."),
        required=False,
    )

    criterion = GlobalInterface(
        title=_("Criterion interface"),
        description=_("Criterion interface"),
        required=False,
    )


class ISchema(Interface):
    """Common edit schema for Faceted Widgets"""

    title = schema.TextLine(
        title=_("Friendly name"),
        description=_("Title for widget to display in view page"),
    )

    placeholder = schema.TextLine(
        title=_("Placeholder"),
        description=_("Text to be displayed as input placeholder"),
        required=False,
    )

    default = schema.TextLine(
        title=_("Default value"), description=_("Default query"), required=False
    )

    index = schema.Choice(
        title=_("Catalog index"),
        description=_("Catalog index to be used"),
        vocabulary="eea.faceted.vocabularies.CatalogIndexes",
    )

    position = schema.Choice(
        title=_("Position"),
        description=_("Widget position in page"),
        vocabulary="eea.faceted.vocabularies.WidgetPositions",
        required=False,
    )

    section = schema.Choice(
        title=_("Section"),
        description=_("Display widget in section"),
        vocabulary="eea.faceted.vocabularies.WidgetSections",
        required=False,
    )

    hidden = schema.Bool(
        title=_("Hidden"), description=_("Hide widget"), required=False
    )

    count = schema.Bool(
        title=_("Count results"),
        description=_("Display number of results near each option"),
        required=False,
    )

    sortcountable = schema.Bool(
        title=_("Sort by countable"),
        description=_("Use the results counter for sorting"),
        required=False,
    )

    hidezerocount = schema.Bool(
        title=_("Hide items with zero results"),
        description=_("This option works only if 'count results' is enabled"),
        required=False,
    )

    custom_css = schema.TextLine(
        title=_("Custom CSS"),
        description=_("Custom CSS class for widget to display in view page"),
        required=False,
    )


class FacetedSchemata(group.Group):
    """Faceted Schemata"""

    prefix = "faceted"


class DefaultSchemata(FacetedSchemata):
    """Schemata default"""

    label = "default"
    fields = field.Fields(ISchema).select("title", "default", "index")


class LayoutSchemata(FacetedSchemata):
    """Schemata layout"""

    label = "layout"
    fields = field.Fields(ISchema).select("position", "section", "hidden", "custom_css")


class CountableSchemata(FacetedSchemata):
    """Schemata countable"""

    label = "countable"
    fields = field.Fields(ISchema).select("count", "sortcountable", "hidezerocount")
