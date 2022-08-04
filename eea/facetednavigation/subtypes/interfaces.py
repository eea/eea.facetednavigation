""" Subtypes interfaces
"""
from zope.interface import Interface


class IPossibleFacetedNavigable(Interface):
    """All objects that should have the ability to be faceted navigable
    should implement this interface.
    """


class IFacetedNavigable(Interface):
    """Marker interface for faceted navigable objects"""


class IFacetedSearchMode(Interface):
    """Marker interface for faceted navigable objects that are used as search
    forms (no default items on load)
    """


IFacetedSearch = IFacetedSearchMode


class IFacetedWrapper(Interface):
    """Wrapper for faceted navigable objects"""


class IFacetedSubtyper(Interface):
    """Support for subtyping objects"""

    def can_enable():
        """Can enable faceted navigation"""

    def can_disable():
        """Can disable faceted navigation"""

    def is_faceted():
        """Is current object faceted navigable"""

    def enable():
        """Enable faceted navigation"""

    def disable():
        """Disable faceted navigation"""
