""" CSS
"""
from App.Common import rfc1123_date
from DateTime import DateTime
from zope.component import getUtility, getMultiAdapter
from zope.interface import directlyProvidedBy, directlyProvides
from zope.publisher.browser import TestRequest
from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.tools.packer import CSSPacker

from eea.facetednavigation.interfaces import IWidgetsInfo

class CSS(object):
    """ Handle criteria
    """
    def __init__(self, context, request, resources=()):
        self.context = context
        self.request = request
        self._resources = resources
        self.duration = 3600*24*365

        self.csstool = getToolByName(context, 'portal_css')
        self.debug = self.csstool.getDebugMode()

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
                content = CSSPacker('safe').pack(content)
            output.append(header + content)
        return '\n'.join(output)

    @property
    def helper_css(self):
        """ Helper css
        """
        info = getUtility(IWidgetsInfo).widgets
        res = []
        for widget in info.values():
            schema = widget.view_schema
            atfields = schema.fields()
            for atfield in atfields:
                atwidget = atfield.widget
                helper = getattr(atwidget, 'helper_css', None)
                 # We expect the attribute value to be a iterable.
                if not helper:
                    continue
                res.extend(item for item in helper if item not in res)
        return res

class ViewCSS(CSS):
    """ CSS libs used in view mode
    """
    @property
    def css_libs(self):
        """ Faceted CSS libs
        """
        return [
            '++resource++eea.faceted-navigation.css',
        ]

    @property
    def resources(self):
        """ Return view resources
        """
        res = self.helper_css
        res.extend(self.css_libs)
        info = getUtility(IWidgetsInfo).widgets
        for widget in info.values():
            view_css = widget.view_css
            if isinstance(view_css, (tuple, list, set)):
                res.extend(css for css in view_css if css not in res)
            elif view_css not in res:
                res.append(view_css)
        return res

    def __call__(self, *args, **kwargs):
        """ view.css
        """
        self.request.RESPONSE.setHeader('content-type', 'text/css')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader(
            'Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()

class EditCSS(CSS):
    """ CSS libs used in edit form
    """
    @property
    def css_libs(self):
        """ Faceted CSS libs
        """
        return [
            '++resource++eea.faceted-navigation-edit.css',
        ]

    @property
    def resources(self):
        """ Return edit resources
        """
        res = self.helper_css
        res.extend(self.css_libs)

        info = getUtility(IWidgetsInfo).widgets
        for widget in info.values():
            edit_css = widget.edit_css
            if isinstance(edit_css, (tuple, list, set)):
                res.extend(css for css in edit_css if css not in res)
            elif edit_css not in res:
                res.append(edit_css)
        return res

    def __call__(self, *args, **kwargs):
        """ edit.css
        """
        self.request.RESPONSE.setHeader('content-type', 'text/css')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader(
            'Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()
