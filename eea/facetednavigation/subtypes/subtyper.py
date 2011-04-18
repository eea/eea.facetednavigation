""" Subtyping support
"""
from zope.interface import implements
from zope.interface import alsoProvides, noLongerProvides
from zope.event import notify

from p4a.subtyper.engine import SubtypeAddedEvent, SubtypeRemovedEvent
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.subtypes.interfaces import IFacetedSubtyper
from eea.facetednavigation.interfaces import IPossibleFacetedNavigable
from eea.facetednavigation.interfaces import IFacetedNavigable

class FacetedSubtyper(BrowserView):
    """ Support for subtyping objects
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
                IStatusMessage(self.request).addStatusMessage(
                    str(msg), type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    @property
    def can_enable(self):
        """ See IFacetedSubtyper
        """
        if not IPossibleFacetedNavigable.providedBy(self.context):
            return False

        if IFacetedNavigable.providedBy(self.context):
            return False
        return True

    @property
    def can_disable(self):
        """ See IFacetedSubtyper
        """
        if not IPossibleFacetedNavigable.providedBy(self.context):
            return False

        if IFacetedNavigable.providedBy(self.context):
            return True
        return False

    @property
    def is_faceted(self):
        """ Is faceted navigable?
        """
        if IFacetedNavigable.providedBy(self.context):
            return True
        return False

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

        if not IFacetedNavigable.providedBy(self.context):
            alsoProvides(self.context, IFacetedNavigable)
        notify(SubtypeAddedEvent(self.context, None))
        self._redirect('Faceted navigation enabled')

    def disable(self):
        """ See IFacetedSubtyper
        """
        if not self.can_disable:
            return self._redirect('Faceted navigation not supported')

        if IFacetedNavigable.providedBy(self.context):
            noLongerProvides(self.context, IFacetedNavigable)
        notify(SubtypeRemovedEvent(self.context, None))
        self._redirect('Faceted navigation disabled')
