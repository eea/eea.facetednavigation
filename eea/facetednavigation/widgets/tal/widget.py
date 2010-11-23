""" ETag widget
"""
# Python
import logging

# Zope2
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.utils import getToolByName


# Zope3
from zope.app.pagetemplate.engine import TrustedEngine, TrustedZopeContext
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

# Package
from eea.facetednavigation.widgets.field import StringField
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

logger = logging.getLogger('eea.facetednavigation.widgets.tal')

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.CatalogIndexes',
        widget=SelectionWidget(
            label='Catalog index',
            label_msgid='faceted_criteria_index',
            description='Catalog index to use for search',
            description_msgid='help_faceted_criteria_index',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('default',
        schemata="default",
        default='string:',
        widget=StringWidget(
            label='Tal Expression',
            label_msgid='faceted_criteria_tal_default',
            description='Default tal expression for query value',
            description_msgid='help_faceted_criteria_tal_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

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
    widget_label = 'TAL Expression'
    edit_css = '++resource++eea.facetednavigation.widgets.tal.edit.css'
    edit_js = '++resource++eea.facetednavigation.widgets.tal.edit.js'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'TAL Expression'
    edit_schema['hidden'].default = True
    edit_schema['hidden'].schemata = 'hidden'

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
        except Exception, err:
            return default

        if path == self.context.absolute_url(1):
            return default

        if IBaseObject.providedBy(referer):
            return referer

        path = '/'.join(path.split('/')[:-1])
        return self.referer(path)

    @property
    def talexpr(self):
        """ Compile tal expression
        """
        talexpr = self.default
        if not talexpr:
            return talexpr

        engine = TrustedEngine
        context = TrustedZopeContext(engine, dict(
            context=self.context.aq_inner,
            referer=self.referer(),
            request=self.request,
            criterion=self.data,
            widget=self
        ))
        expression = engine.compile(talexpr)
        return context.evaluate(expression)

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
            value = self.talexpr
        except Exception, err:
            logger.exception(err)
            return query

        if value == "FACET-EMPTY":
            return query

        query[index] = value
        logger.debug(query)

        return query
