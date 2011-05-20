""" Schemas
"""
from zope.i18nmessageid.message import MessageFactory
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView

PMF = MessageFactory('plone')


class Schema(BrowserView):
    """ Handle widgets in edit mode
    """
    index = ZopeTwoPageTemplateFile('schema.pt', globals())

    def __init__(self, context, request, widget, data):
        self.context = context
        self.request = request
        self.request.debug = False
        self.widget = widget(context, request, data)
        self.data = data

    def __call__(self, **kwargs):
        return self.index()

    def getTranslatedSchemaLabel(self, schema):
        """Get message for schemata
        """
        label = u"label_schema_%s" % schema
        default = unicode(schema).capitalize()
        return PMF(label, default=default)
