""" Widgets interfaces
"""
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
