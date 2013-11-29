""" Javascript
"""
from App.Common import rfc1123_date
from DateTime import DateTime
from zope.component import getUtility, getMultiAdapter
from zope.interface import directlyProvidedBy, directlyProvides
from zope.publisher.browser import TestRequest
from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.tools.packer import JavascriptPacker

from eea.facetednavigation.interfaces import IWidgetsInfo

class Javascript(object):
    """ Handle criteria
    """
    def __init__(self, context, request, resources=()):
        self.context = context
        self.request = request
        self._resources = resources
        self.duration = 3600*24*365

        self.jstool = getToolByName(context, 'portal_javascripts')
        self.debug = self.jstool.getDebugMode()

    @property
    def resources(self):
        """ Return resources
        """
        return self._resources

    def get_resource(self, resource):
        """ Get resource content
        """
        # If resources are retrieved via GET, the request headers
        # are used for caching AND are mangled.
        # That can result in getting 304 responses
        # There is no API to extract the data from the view without
        # mangling the headers, so we must use a fake request
        # that can be modified without harm
        if resource.startswith('++resource++'):
            fake_request = TestRequest()
            # copy interfaces that may have been applied to the request to
            # the TestRequest:
            directlyProvides(fake_request, directlyProvidedBy(self.request))
            traverser = getMultiAdapter((self.context, fake_request),
                name='resource')
            obj = traverser.traverse(resource[12:], None)
        else:
            obj = self.context.restrictedTraverse(resource, None)
        if not obj:
            return '/* ERROR */'
        try:
            content = obj.GET()
        except AttributeError, err:
            return str(obj)
        except Exception, err:
            return '/* ERROR: %s */' % err
        else:
            return content

    def get_content(self, **kwargs):
        """ Get content
        """
        output = []
        for resource in self.resources:
            content = self.get_resource(resource)
            header = '\n/* - %s - */\n' % resource
            if not self.debug:
                content = JavascriptPacker('safe').pack(content)
            output.append(header + content)
        return '\n'.join(output)

    @property
    def helper_js(self):
        """ Helper js
        """
        info = getUtility(IWidgetsInfo).widgets
        res = []
        for widget in info.values():
            schema = widget.view_schema
            atfields = schema.fields()
            for atfield in atfields:
                atwidget = atfield.widget
                helper = getattr(atwidget, 'helper_js', None)
                # We expect the attribute value to be a iterable.
                if not helper:
                    continue
                res.extend(item for item in helper if item not in res)
        return res

class ViewJavascript(Javascript):
    """ Javascript libs used in view mode
    """
    @property
    def js_libs(self):
        """ JS Libs
        """
        return ['++resource++eea.faceted-navigation.js',
                '++resource++eea.faceted-navigation-expand.js',
                '++resource++eea.faceted-navigation-independent.js']

    @property
    def resources(self):
        """ Return view resources
        """
        res = self.helper_js
        res.extend(self.js_libs)
        info = getUtility(IWidgetsInfo).widgets
        for widget in info.values():
            view_js = widget.view_js
            if isinstance(view_js, (tuple, list, set)):
                res.extend(js for js in view_js if js not in res)
            elif view_js not in res:
                res.append(view_js)
        return res

    def __call__(self, *args, **kwargs):
        """ view.js
        """
        self.request.RESPONSE.setHeader('content-type', 'text/javascript')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader(
            'Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()

class EditJavascript(Javascript):
    """ Javascript libs used in edit form
    """
    @property
    def js_libs(self):
        """ JS libs
        """
        return [
            '++resource++eea.faceted-navigation-edit.js',
            '++resource++eea.faceted-navigation-expand.js'
        ]

    @property
    def resources(self):
        """ Return edit resources
        """
        res = self.helper_js
        res.extend(self.js_libs)

        info = getUtility(IWidgetsInfo).widgets
        for widget in info.values():
            edit_js = widget.edit_js
            if isinstance(edit_js, (tuple, list, set)):
                res.extend(js for js in edit_js if js not in res)
            elif edit_js not in res:
                res.append(edit_js)
        return res

    def __call__(self, *args, **kwargs):
        """ edit.js
        """
        self.request.RESPONSE.setHeader('content-type', 'text/javascript')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader(
            'Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()
