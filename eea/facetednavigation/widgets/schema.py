from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView

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
