""" Faceted events
"""
from zope.interface import implementer
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

@implementer(IFacetedEvent)
class FacetedEvent(ObjectEvent):
    """ Abstract faceted event. All faceted events should inherit from it """


@implementer(IFacetedGlobalSettingsChangedEvent)
class FacetedGlobalSettingsChangedEvent(FacetedEvent):
    """ Sent if faceted navigation global settings were changed """


@implementer(IFacetedWillBeEnabledEvent)
class FacetedWillBeEnabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation is going to be enabled """


@implementer(IFacetedEnabledEvent)
class FacetedEnabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation was enabled """


@implementer(IFacetedWillBeDisabledEvent)
class FacetedWillBeDisabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation is goinf to be disabled """


@implementer(IFacetedDisabledEvent)
class FacetedDisabledEvent(FacetedEvent):
    """ Event triggered if faceted navigation was disabled """


@implementer(IQueryWillBeExecutedEvent)
class QueryWillBeExecutedEvent(FacetedEvent):
    """Event triggered before a query is executed."""

    def __init__(self, obj, query):
        self.object = obj
        self.query = query
