try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.interfaces import IAnnotations

try:
    from zope.annotation.attribute import AttributeAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.attribute import AttributeAnnotations

from zope import schema
from zope.interface import Interface, alsoProvides
from zope.app.content.interfaces import IContentType

class IPossibleFacetedNavigable(Interface):
    """ All objects that should have the ability to be faceted navigable
        should implement this interface.
    """

class IFacetedNavigable(Interface):
    """ Marker interface for faceted navigable objects
    """
alsoProvides(IFacetedNavigable, IContentType)

class IFacetedWrapper(Interface):
    """ Wrapper for faceted navigable objects
    """

class IFacetedSubtyper(Interface):
    """ Support for subtyping objects
    """

    can_enable = schema.Bool(u'Can enable faceted navigation', readonly=True)
    can_disable = schema.Bool(u'Can disable faceted navigation', readonly=True)
    is_faceted = schema.Bool(u'Is current object faceted navigable', readonly=True)
    is_lingua_faceted = schema.Bool(u'Is LinguaPlone installed and current object is faceted navigable', readonly=True)

    def enable():
        """ Enable faceted navigation
        """
        pass

    def disable():
        """Disable faceted navigation
        """
        pass
