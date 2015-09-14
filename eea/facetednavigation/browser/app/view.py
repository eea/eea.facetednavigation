""" Faceted views
"""
from zope.component import getUtility
from zope.component import queryAdapter
from zope.schema.interfaces import IVocabularyFactory
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedWrapper
from eea.facetednavigation.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.interfaces import IHidePloneRightColumn
from eea.facetednavigation.interfaces import IDisableSmartFacets
from eea.facetednavigation.interfaces import IFacetedSearchMode
from eea.facetednavigation.settings.interfaces import IDontInheritConfiguration
from Products.Five.browser import BrowserView
from Products.CMFPlone.resources import add_bundle_on_request

class FacetedContainerView(object):
    """ Faceted view
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        add_bundle_on_request(request, 'facetednavigation-jquery')
        add_bundle_on_request(request, 'facetednavigation-view')
        self._canonical = '<NOT SET>'

    @property
    def mode(self):
        """ Display mode
        """
        if (IFacetedSearchMode.providedBy(self.canonical) or
            IFacetedSearchMode.providedBy(self.context)):
            return 'search'
        return 'view'

    @property
    def canonical(self):
        """ Get canonical
        """
        if not IDontInheritConfiguration.providedBy(self.context):
            if self._canonical == '<NOT SET>':
                canonical = getattr(self.context, 'getCanonical', None)
                if callable(canonical):
                    canonical = canonical()
                self._canonical = canonical
        return self._canonical

    @property
    def positions(self):
        """ Return available columns
        """
        voc = getUtility(IVocabularyFactory,
                         'eea.faceted.vocabularies.WidgetPositions')
        return voc(self.context)

    @property
    def hide_left_column(self):
        """ Disable plone portlets left column
        """
        return (IHidePloneLeftColumn.providedBy(self.canonical) or
                IHidePloneLeftColumn.providedBy(self.context))

    @property
    def hide_right_column(self):
        """ Disable plone portlets right column
        """
        return (IHidePloneRightColumn.providedBy(self.canonical) or
                IHidePloneRightColumn.providedBy(self.context))

    @property
    def disable_smart_facets(self):
        """ Disable 'smart facets hiding'
        """
        return (IDisableSmartFacets.providedBy(self.canonical) or
                IDisableSmartFacets.providedBy(self.context))

    def get_context(self, content=None):
        """ Return context
        """
        wrapper = queryAdapter(self.context, IFacetedWrapper)
        if not wrapper:
            return self.context
        return wrapper(content)

    def get_sections(self, position='', mode='view'):
        """ Get sections for given position or return all sections
        """
        voc = getUtility(IVocabularyFactory,
                         'eea.faceted.vocabularies.WidgetSections')
        voc = voc(self.context)
        if not position or mode not in ('view', 'search'):
            return [t for t in voc]

        widgets = self.get_view_widgets(position=position)
        sections = [widget.data.get('section') for widget in widgets]
        return [term for term in voc if term.value in sections]

    def get_view_widgets(self, position='', section=''):
        """ Get not hidden widgets
        """
        widgets = self.get_widgets(position, section)
        for widget in widgets:
            if widget.hidden:
                continue
            yield widget

    def get_widgets(self, position='', section=''):
        """ Get all widgets
        """
        criteria = ICriteria(self.context)
        for criterion in criteria.values():
            if position and criterion.get('position', 'right') != position:
                continue
            if section and criterion.get('section', 'default') != section:
                continue
            widget = criteria.widget(wid=criterion.get('widget'))
            yield widget(self.context, self.request, criterion)

    def check_display_criteria(self, faceted_html):
        """ Check criteria
        """
        if self.disable_smart_facets:
            return True
        return self.context.unrestrictedTraverse(
            '@@faceted_display_criteria_checker').check(faceted_html)


class DisplayCriteriaCheckerView(BrowserView):
    """This views checks if criteria are displayed on faceted navigation
    """
    def check(self, faceted_html):
        """ Check
        """
        if 'listingBar' in faceted_html:
            return True
        elif self.language_present():
            return True
        else:
            return False

    def language_present(self):
        """ Is there any widget for Language index?
        """

        criteria = ICriteria(self.context)
        for criterion in criteria.values():
            if criterion.get('index', None) == 'Language':
                if not criterion.hidden:
                    return True
        return False
