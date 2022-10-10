""" Faceted Navigation public interfaces
"""
from eea.facetednavigation import _

# Criteria
from eea.facetednavigation.criteria.interfaces import ICriteria

# Language
from eea.facetednavigation.indexes.language.interfaces import ILanguageWidgetAdapter

# Layout
from eea.facetednavigation.layout.interfaces import IFacetedLayout

# Search
from eea.facetednavigation.search.interfaces import IFacetedCatalog

# Settings
from eea.facetednavigation.settings.interfaces import IDisableSmartFacets
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn

# Wrapper
# Subtypes
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from eea.facetednavigation.subtypes.interfaces import IFacetedSearchMode
from eea.facetednavigation.subtypes.interfaces import IFacetedWrapper
from eea.facetednavigation.subtypes.interfaces import IPossibleFacetedNavigable

# Versioning
from eea.facetednavigation.versions.interfaces import IFacetedVersion

# Faceted Views
from eea.facetednavigation.views.interfaces import IViewsInfo

# After query adapter
# Widgets
from eea.facetednavigation.widgets.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import IWidgetFilterBrains
from eea.facetednavigation.widgets.interfaces import IWidgetsInfo
from zope import schema
from zope.interface import Interface
from zope.interface.interfaces import IObjectEvent


#
# Events
#
class IFacetedEvent(IObjectEvent):
    """All faceted events should inherit from this class"""


class IFacetedSettingsWillBeChangedEvent(IFacetedEvent):
    """Faceted settings will be updated"""


class IFacetedGlobalSettingsChangedEvent(IFacetedEvent):
    """Faceted global settings updated"""


class IFacetedWillBeEnabledEvent(IFacetedEvent):
    """Faceted navigation is going to be enabled"""


class IFacetedEnabledEvent(IFacetedEvent):
    """Faceted navigation enabled"""


class IFacetedWillBeDisabledEvent(IFacetedEvent):
    """Faceted navigation is going to be disabled"""


class IFacetedDisabledEvent(IFacetedEvent):
    """Faceted navigation disabled"""


class IEEASettings(Interface):
    """Registry settings for eea.facetednavigation product"""

    disable_diazo_rules_ajax = schema.Bool(
        title=_("Disable diazo rules on ajax requests"), required=False
    )


class IQueryWillBeExecutedEvent(IFacetedEvent):
    """Catalog query event."""

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
