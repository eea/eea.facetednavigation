""" Faceted events
"""
from zope.interface import implements
from zope.component.interfaces import ObjectEvent
from eea.facetednavigation.interfaces import (
    IFacetedEvent,
    IFacetedGlobalSettingsChangedEvent,
    IFacetedWillBeEnabledEvent,
    IFacetedEnabledEvent,
    IFacetedWillBeDisabledEvent,
    IFacetedDisabledEvent,
    IQueryWillBeExecutedEvent,
)

class FacetedEvent(ObjectEvent):
    """ Abstract faceted event. All faceted events should inherit from it """
    implements(IFacetedEvent)

class FacetedGlobalSettingsChangedEvent(FacetedEvent):
    """ Sent if faceted navigation global settings were changed """
    implements(IFacetedGlobalSettingsChangedEvent)

class FacetedWillBeEnabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation is going to be enabled """
    implements(IFacetedWillBeEnabledEvent)

class FacetedEnabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation was enabled """
    implements(IFacetedEnabledEvent)

class FacetedWillBeDisabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation is goinf to be disabled """
    implements(IFacetedWillBeDisabledEvent)

class FacetedDisabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation was disabled """
    implements(IFacetedDisabledEvent)


class QueryWillBeExecutedEvent(FacetedEvent):
    """Event triggered before a query is executed."""
    implements(IQueryWillBeExecutedEvent)

    def __init__(self, obj, query):
        self.object = obj
        self.query = query
