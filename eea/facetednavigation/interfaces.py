try:
    from zope.component.interfaces import IObjectEvent
except ImportError:
    #BBB Plone 2.5
    from zope.app.event.interfaces import IObjectEvent


# Subtypes
from eea.facetednavigation.subtypes.interfaces import IPossibleFacetedNavigable
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable

# Criteria
from eea.facetednavigation.criteria.interfaces import ICriteria

# Layout
from eea.facetednavigation.layout.interfaces import IFacetedLayout

# Search
from eea.facetednavigation.search.interfaces import IFacetedCatalog

# Widgets
from eea.facetednavigation.widgets.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import IWidgetsInfo

# After query adapter
from eea.facetednavigation.widgets.interfaces import IWidgetFilterBrains

# Language
from eea.facetednavigation.indexes.language.interfaces import ILanguageWidgetAdapter

# Versioning
from eea.facetednavigation.versions.interfaces import IFacetedVersion

# Wrapper
from eea.facetednavigation.subtypes.interfaces import IFacetedWrapper

#
# Events
#
class IFacetedEvent(IObjectEvent):
    """ All faceted events should inherit from this class
    """

class IFacetedGlobalSettingsChangedEvent(IFacetedEvent):
    """ Faceted global settings updated
    """
