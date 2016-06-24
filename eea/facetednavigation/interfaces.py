""" Faceted Navigation public interfaces
"""
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface
from zope import schema

# Subtypes
from eea.facetednavigation.subtypes.interfaces import IPossibleFacetedNavigable
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from eea.facetednavigation.subtypes.interfaces import IFacetedSearchMode

# Criteria
from eea.facetednavigation.criteria.interfaces import ICriteria

# Layout
from eea.facetednavigation.layout.interfaces import IFacetedLayout

# Search
from eea.facetednavigation.search.interfaces import IFacetedCatalog

# Widgets
from eea.facetednavigation.widgets.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import IWidgetsInfo

# Faceted Views
from eea.facetednavigation.views.interfaces import IViewsInfo

# After query adapter
from eea.facetednavigation.widgets.interfaces import IWidgetFilterBrains

# Language
from eea.facetednavigation.indexes.language.interfaces import (
    ILanguageWidgetAdapter,
)

# Versioning
from eea.facetednavigation.versions.interfaces import IFacetedVersion

# Wrapper
from eea.facetednavigation.subtypes.interfaces import IFacetedWrapper

# Settings
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn
from eea.facetednavigation.settings.interfaces import IDisableSmartFacets
from eea.facetednavigation import EEAMessageFactory as _
#
# Events
#
class IFacetedEvent(IObjectEvent):
    """ All faceted events should inherit from this class
    """

class IFacetedGlobalSettingsChangedEvent(IFacetedEvent):
    """ Faceted global settings updated
    """

class IFacetedWillBeEnabledEvent(IFacetedEvent):
    """ Faceted navigation is going to be enabled
    """

class IFacetedEnabledEvent(IFacetedEvent):
    """ Faceted navigation enabled
    """

class IFacetedWillBeDisabledEvent(IFacetedEvent):
    """ Faceted navigation is going to be disabled
    """

class IFacetedDisabledEvent(IFacetedEvent):
    """ Faceted navigation disabled
    """


class IEEASettings(Interface):
    """ Registry settings for eea.facetednavigation product
    """

    disable_diazo_rules_ajax = schema.Bool(
                title=_(u"Disable diazo rules on ajax requests"),
                required=False)


class IQueryWillBeExecutedEvent(IFacetedEvent):
    """ Catalog query event.
    """

    # query = Attribute(u"The query that will be done.")


# pylint, pyflakes
__all__ = [
    IPossibleFacetedNavigable.__name__,
    IFacetedNavigable.__name__,
    IFacetedSearchMode.__name__,
    IWidgetsInfo.__name__,
    IViewsInfo.__name__,
    IWidgetFilterBrains.__name__,
    IFacetedCatalog.__name__,
    IFacetedLayout.__name__,
    IFacetedVersion.__name__,
    ILanguageWidgetAdapter.__name__,
    ICriteria.__name__,
    IFacetedWrapper.__name__,
    IWidget.__name__,
    IHidePloneLeftColumn.__name__,
    IHidePloneRightColumn.__name__,
    IDisableSmartFacets.__name__,
    IQueryWillBeExecutedEvent.__name__,
]
