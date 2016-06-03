""" Widgets interfaces
"""
from zope import schema
from zope.interface import Interface
from zope.configuration.fields import GlobalObject
from zope.i18nmessageid import ZopeMessageFactory as _

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

class ICommonEditSchema(Interface):
    """ Common edit schema for Faceted Widgets
    """
    # Schemata default
    title = schema.TextLine(
        title=_(u"Friendly name"),
        description=_(u"Title for widget to display in view page")
    )

    # Schemata layout
    position = schema.Choice(
        title=_(u'Position'),
        description=_(u"Widget position in page"),
        vocabulary="eea.faceted.vocabularies.WidgetPositions"
    )

    # schemata="layout",
    section = schema.Choice(
        title=_(u"Section"),
        description=_("Display widget in section"),
        vocabulary="eea.faceted.vocabularies.WidgetSections",
    )

    # schemata="layout",
    hidden = schema.Bool(
        title=_(u'Hidden'),
        description=_(u"Hide widget"),
    )
