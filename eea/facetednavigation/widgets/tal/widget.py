""" TAL widget
"""
# Python
import logging
from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets import TrustedEngine
from eea.facetednavigation.widgets import TrustedZopeContext
from eea.facetednavigation.widgets.tal.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.tal.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _
logger = logging.getLogger('eea.facetednavigation.widgets.tal')


class Widget(AbstractWidget):
    """ TAL Expression widget

    The following contexts can be used within tal expressions:

    context   -- faceted navigable context
    referer   -- request.HTTP_REFERER object. Use this if you load
                 faceted from another place (like: portal_relations)
    request   -- faceted navigable REQUEST object
    widget    -- Tal Expression Widget instance
    criterion -- Tal Expression Criterion instance

    """
    widget_type = 'tal'
    widget_label = _('TAL Expression')

    index = ViewPageTemplateFile('widget.pt')
    groups = (DefaultSchemata, LayoutSchemata)

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

    def talexpr(self, form=None):
        """ Compile tal expression
        """
        if form is None:
            form = {}

        talexpr = self.default
        if talexpr is None:
            return ''

        engine = TrustedEngine
        context = TrustedZopeContext(engine, dict(
            context=self.context.aq_inner,
            referer=self.referer(),
            request=self.request,
            criterion=self.data,
            widget=self,
            form=form
        ))
        expression = engine.compile(talexpr)
        result = context.evaluate(expression)
        if callable(result):
            return result()
        return result

    def query(self, form):
        """ Update query.

        Use 'FACET-EMPTY' string to send no query to catalog
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        try:
            value = self.talexpr(form=form)
        except Exception, err:
            logger.exception(err)
            return query

        if value == "FACET-EMPTY":
            return query

        query[index] = value
        logger.debug(query)

        return query
