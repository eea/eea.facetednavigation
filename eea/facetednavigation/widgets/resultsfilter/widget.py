""" Results Filter widget
"""
import logging
from zope.interface import implementer
from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.widgets import TrustedEngine
from eea.facetednavigation.widgets import TrustedZopeContext
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.resultsfilter.interfaces import (
    IResultsFilterWidget,
    DefaultSchemata,
    LayoutSchemata,
)
logger = logging.getLogger('eea.facetednavigation.widgets.resultsfilter')


@implementer(IResultsFilterWidget)
class Widget(AbstractWidget):
    """ Results Filter widget

    The following contexts can be used within tal expressions:

    context   -- faceted navigable context
    referer   -- request.HTTP_REFERER object. Use this if you load
                 faceted from another place (like: portal_relations)
    request   -- faceted navigable REQUEST object
    widget    -- Results Filter Widget instance
    criterion -- Results Filter Criterion instance
    brain     -- Catalog brain

    """
    widget_type = 'resultsfilter'
    widget_label = _('Results Filter')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')

    def referer(self, path=None):
        """ Extract referer from request or return self.context
        """
        default = self.context.aq_inner
        if path is None:
            path = getattr(self.request, 'HTTP_REFERER', None)

        if not path:
            return default

        portal_url = getToolByName(self.context, 'portal_url')
        path = path.replace(portal_url(), '', 1)
        site = portal_url.getPortalObject().absolute_url(1)
        if site and (not path.startswith(site)):
            path = site + path

        try:
            referer = self.context.restrictedTraverse(path)
        except Exception:
            return default

        if path == self.context.absolute_url(1):
            return default

        if IBaseObject.providedBy(referer):
            return referer

        path = '/'.join(path.split('/')[:-1])
        return self.referer(path)

    def talexpr(self, brain=None):
        """ Compile tal expression
        """
        talexpr = self.default
        if talexpr is None:
            return ''

        engine = TrustedEngine
        context = TrustedZopeContext(engine, dict(
            context=self.context.aq_inner,
            referer=self.referer(),
            request=self.request,
            criterion=self.data,
            brain=brain,
            widget=self
        ))
        expression = engine.compile(talexpr)
        result = context.evaluate(expression)
        if callable(result):
            return result()
        return result
