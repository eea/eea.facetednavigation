""" Subtyping support
"""
from zope.interface import implements
from zope.interface import alsoProvides, noLongerProvides
from zope.event import notify
from zope.publisher.interfaces import NotFound

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from eea.facetednavigation.subtypes.interfaces import IFacetedSubtyper
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import IFacetedSearchMode
from eea.facetednavigation.interfaces import IDisableSmartFacets
from eea.facetednavigation.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.interfaces import IHidePloneRightColumn
from eea.facetednavigation.events import (
    FacetedWillBeDisabledEvent,
    FacetedWillBeEnabledEvent,
    FacetedDisabledEvent,
    FacetedEnabledEvent,
)
from eea.facetednavigation import EEAMessageFactory as _


class FacetedPublicSubtyper(BrowserView):
    """ Public support for subtyping objects
        view for non IPossibleFacetedNavigable objects
    """
    implements(IFacetedSubtyper)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg=''):
        """ Redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(msg, type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    @property
    def can_enable(self):
        """ See IFacetedSubtyper
        """
        return False

    @property
    def can_disable(self):
        """ See IFacetedSubtyper
        """
        return False

    @property
    def is_faceted(self):
        """ Is faceted navigable?
        """
        return False

    @property
    def is_lingua_faceted(self):
        """ Is LinguaPlone installed and context is faceted navigable?
        """
        return False

    def enable(self):
        """ See IFacetedSubtyper
        """
        raise NotFound(self.context, 'enable', self.request)

    def disable(self):
        """ See IFacetedSubtyper
        """
        raise NotFound(self.context, 'disable', self.request)


class FacetedSubtyper(FacetedPublicSubtyper):
    """ Support for subtyping objects
        view for IPossibleFacetedNavigable objects
    """

    @property
    def can_enable(self):
        """ See IFacetedSubtyper
        """
        return not self.is_faceted

    @property
    def can_disable(self):
        """ See IFacetedSubtyper
        """
        return self.is_faceted

    @property
    def is_faceted(self):
        """ Is faceted navigable?
        """
        return IFacetedNavigable.providedBy(self.context)

    @property
    def is_lingua_faceted(self):
        """ Is LinguaPlone installed and context is faceted navigable?
        """
        if not self.is_faceted:
            return False
        qtool = getToolByName(self.context, 'portal_quickinstaller')
        installed = [package['id'] for package in qtool.listInstalledProducts()]
        if 'LinguaPlone' not in installed:
            return False
        return True

    def enable(self):
        """ See IFacetedSubtyper
        """
        if not self.can_enable:
            return self._redirect('Faceted navigation not supported')

        notify(FacetedWillBeEnabledEvent(self.context))
        alsoProvides(self.context, IFacetedNavigable)
        if not IDisableSmartFacets.providedBy(self.context):
            alsoProvides(self.context, IDisableSmartFacets)
        if not IHidePloneLeftColumn.providedBy(self.context):
            alsoProvides(self.context, IHidePloneLeftColumn)
        if not IHidePloneRightColumn.providedBy(self.context):
            alsoProvides(self.context, IHidePloneRightColumn)
        notify(FacetedEnabledEvent(self.context))

        self._redirect(_('Faceted navigation enabled'))

    def disable(self):
        """ See IFacetedSubtyper
        """
        if not self.can_disable:
            return self._redirect('Faceted navigation not supported')

        notify(FacetedWillBeDisabledEvent(self.context))
        noLongerProvides(self.context, IFacetedNavigable)
        notify(FacetedDisabledEvent(self.context))
        self._redirect(_('Faceted navigation disabled'))

class FacetedSearchSubtyper(FacetedSubtyper):
    """ Support for subtyping objects as faceted search form (no default items
        on load)
    """
    @property
    def is_faceted(self):
        """ Is faceted navigable?
        """
        if not super(FacetedSearchSubtyper, self).is_faceted:
            return False
        return IFacetedSearchMode.providedBy(self.context)

    def enable(self):
        """ See IFacetedSubtyper
        """
        if not self.can_enable:
            return self._redirect('Faceted search navigation not supported')

        if not super(FacetedSearchSubtyper, self).is_faceted:
            super(FacetedSearchSubtyper, self).enable()
        if not IFacetedSearchMode.providedBy(self.context):
            alsoProvides(self.context, IFacetedSearchMode)
        self._redirect(_('Faceted search enabled'))

    def disable(self):
        """ See IFacetedSubtyper
        """
        if not self.can_disable:
            return self._redirect('Faceted search navigation not supported')
        noLongerProvides(self.context, IFacetedSearchMode)
        self._redirect(_('Faceted search disabled'))
