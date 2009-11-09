""" Subtyping support
"""
from zope.interface import implements
from zope.component import getUtility

from p4a.subtyper.interfaces import ISubtyper
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from interfaces import IFacetedSubtyper

class FacetedSubtyper(BrowserView):
    """ Support for subtyping objects
    """
    implements(IFacetedSubtyper)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.subtyper = getUtility(ISubtyper)

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
        existing = self.subtyper.existing_type(self.context)
        if existing and existing.name.startswith('eea.facetednavigation.'):
            return False
        return True

    @property
    def can_disable(self):
        """ See IFacetedSubtyper
        """
        existing = self.subtyper.existing_type(self.context)
        if existing and existing.name.startswith('eea.facetednavigation.'):
            return True
        return False

    def enable(self):
        """ See IFacetedSubtyper
        """
        possible_types = [subtype.name for subtype
                          in self.subtyper.possible_types(self.context) if
                          subtype.name.startswith('eea.facetednavigation.')]

        if not possible_types:
            return self._redirect("This object is not faceted navigable")

        subtype = possible_types[0]
        self.subtyper.change_type(self.context, subtype)
        self._redirect('Faceted navigation enabled')

    def disable(self):
        """ See IFacetedSubtyper
        """
        existing = self.subtyper.existing_type(self.context)
        if existing and existing.name.startswith('eea.facetednavigation.'):
            self.subtyper.remove_type(self.context)
        self._redirect('Faceted navigation disabled')
