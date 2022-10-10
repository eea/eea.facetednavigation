""" Schemas
"""
from zope.i18nmessageid.message import MessageFactory
from zope.publisher.browser import BrowserPage
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import safe_unicode

_ = MessageFactory("plone")


class Schema(BrowserPage):
    """Handle widgets in edit mode"""

    template = ViewPageTemplateFile("schema.pt")

    def __init__(self, context, request, widget, data):
        self.context = context
        self.request = request
        self.request.debug = False
        self.widget = widget(context, request, data)
        self.data = data

    def __call__(self, **kwargs):
        self.widget.update()
        return self.template()

    def getTranslatedSchemaLabel(self, schema):
        """Get message for schemata"""
        label = "label_schema_%s" % schema
        default = safe_unicode(schema).capitalize()
        return _(label, default=default)
