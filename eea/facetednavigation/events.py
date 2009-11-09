""" Faceted events
"""
from zope.interface import implements
from interfaces import IFacetedGlobalSettingsChangedEvent

class FacetedGlobalSettingsChangedEvent(object):
    """ Sent if faceted navigation global settings were changed """
    implements(IFacetedGlobalSettingsChangedEvent)

    def __init__(self, context):
        self.object = context
