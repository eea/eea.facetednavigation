""" Subtyping support
"""
from eea.facetednavigation import _
from eea.facetednavigation.events import FacetedDisabledEvent
from eea.facetednavigation.events import FacetedEnabledEvent
from eea.facetednavigation.events import FacetedWillBeDisabledEvent
from eea.facetednavigation.events import FacetedWillBeEnabledEvent
from eea.facetednavigation.interfaces import IDisableSmartFacets
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import IFacetedSearchMode
from eea.facetednavigation.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.interfaces import IHidePloneRightColumn
from eea.facetednavigation.subtypes.interfaces import IFacetedSubtyper
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.event import notify
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import noLongerProvides
from zope.publisher.interfaces import NotFound

import pkg_resources


plone_version = pkg_resources.get_distribution("Products.CMFPlone").version


@implementer(IFacetedSubtyper)
class FacetedPublicSubtyper(BrowserView):
    """Public support for subtyping objects
    view for non IPossibleFacetedNavigable objects
    """

    def _redirect(self, msg=""):
        """Redirect"""
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(msg, type="info")
            self.request.response.redirect(self.context.absolute_url())
        return msg

    def can_enable(self):
        """See IFacetedSubtyper"""
        return False

    def can_disable(self):
        """See IFacetedSubtyper"""
        return False

    def is_faceted(self):
        """Is faceted navigable?"""
        return False

    def enable(self):
        """See IFacetedSubtyper"""
        raise NotFound(self.context, "enable", self.request)

    def disable(self):
        """See IFacetedSubtyper"""
        raise NotFound(self.context, "disable", self.request)


class FacetedSubtyper(FacetedPublicSubtyper):
    """Support for subtyping objects
    view for IPossibleFacetedNavigable objects
    """

    def can_enable(self):
        """See IFacetedSubtyper"""
        return not self.is_faceted()

    def can_disable(self):
        """See IFacetedSubtyper"""
        return self.is_faceted()

    def is_faceted(self):
        """Is faceted navigable?"""
        return IFacetedNavigable.providedBy(self.context)

    def enable(self):
        """See IFacetedSubtyper"""
        if not self.can_enable():
            return self._redirect("Faceted navigation not supported")

        notify(FacetedWillBeEnabledEvent(self.context))
        alsoProvides(self.context, IFacetedNavigable)
        if not IDisableSmartFacets.providedBy(self.context):
            alsoProvides(self.context, IDisableSmartFacets)
        if not IHidePloneLeftColumn.providedBy(self.context):
            alsoProvides(self.context, IHidePloneLeftColumn)
        if not IHidePloneRightColumn.providedBy(self.context):
            alsoProvides(self.context, IHidePloneRightColumn)
        notify(FacetedEnabledEvent(self.context))

        self._redirect(_("Faceted navigation enabled"))

    def disable(self):
        """See IFacetedSubtyper"""
        if not self.can_disable():
            return self._redirect("Faceted navigation not supported")

        notify(FacetedWillBeDisabledEvent(self.context))
        noLongerProvides(self.context, IFacetedNavigable)
        notify(FacetedDisabledEvent(self.context))
        self._redirect(_("Faceted navigation disabled"))


class FacetedSearchSubtyper(FacetedSubtyper):
    """Support for subtyping objects as faceted search form (no default items
    on load)
    """

    def is_faceted(self):
        """Is faceted navigable?"""
        if not super(FacetedSearchSubtyper, self).is_faceted():
            return False
        return IFacetedSearchMode.providedBy(self.context)

    def enable(self):
        """See IFacetedSubtyper"""
        if not self.can_enable():
            return self._redirect("Faceted search navigation not supported")

        if not super(FacetedSearchSubtyper, self).is_faceted():
            super(FacetedSearchSubtyper, self).enable()
        if not IFacetedSearchMode.providedBy(self.context):
            alsoProvides(self.context, IFacetedSearchMode)
        self._redirect(_("Faceted search enabled"))

    def disable(self):
        """See IFacetedSubtyper"""
        if not self.can_disable():
            return self._redirect("Faceted search navigation not supported")
        noLongerProvides(self.context, IFacetedSearchMode)
        self._redirect(_("Faceted search disabled"))
