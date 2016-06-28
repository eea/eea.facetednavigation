""" Schemas
"""
from zope.i18nmessageid.message import MessageFactory
from zope.publisher.browser import BrowserPage
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

_ = MessageFactory('plone')


class Schema(BrowserPage):
    """ Handle widgets in edit mode
    """
    template = ViewPageTemplateFile('schema.pt')

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
        """Get message for schemata
        """
        label = u"label_schema_%s" % schema
        default = unicode(schema).capitalize()
        return _(label, default=default)
