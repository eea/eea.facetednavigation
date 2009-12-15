from App.Common import rfc1123_date
from DateTime import DateTime
from zope.component import getUtility
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
                [res.append(item) for item in helper if item not in res]
        return res

class ViewJavascript(Javascript):
    """ Javascript libs used in view mode
    """
    @property
    def js_libs(self):
        res = []
        ui_installed = jquery_installed = False
        jtagcloud_installed = False
        for js in self.jstool.getResources():
            if not js.getEnabled():
                continue
            js_id = js.getId()
            if 'jquery.ui' in js_id.lower():
                ui_installed = True
            elif 'jquery.tagcloud' in js_id.lower():
                jtagcloud_installed = True
            #XXX This conflicts with Plone3 default jquery 1.2.x version
            #elif 'jquery' in js_id.lower():
                #jquery_installed = True
            if jquery_installed and jtagcloud_installed and ui_installed:
                break

        if not jquery_installed:
            res.append('++resource++jquery-1.3.2.js')
        if not ui_installed:
            res.append('++resource++jquery.ui-1.7.js')
        if not jtagcloud_installed:
            res.append('++resource++jquery.tagcloud.js')

        res.extend(('++resource++eea.faceted-navigation.js',
                    '++resource++eea.faceted-navigation-expand.js'))
        return res

    @property
    def resources(self):
        """ Return view resources
        """
        res = self.helper_js
        res.extend(self.js_libs)
        info = getUtility(IWidgetsInfo).widgets
        for widget in info.values():
            view_js = widget.view_js
            if isinstance(view_js, tuple):
                res.extend(view_js)
            else:
                res.append(view_js)
        return res

    def __call__(self, *args, **kwargs):
        """ view.js
        """
        self.request.RESPONSE.setHeader('content-type', 'text/javascript')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()

class EditJavascript(Javascript):
    """ Javascript libs used in edit form
    """
    @property
    def js_libs(self):
        res = []
        jquery_installed = ui_installed = False
        cookie_installed = jtagcloud_installed = False
        jfileupload_installed = False
        for js in self.jstool.getResources():
            if not js.getEnabled():
                continue
            js_id = js.getId()
            if 'jquery.ui' in js_id.lower():
                ui_installed = True
            elif 'jquery.cookie' in js_id.lower():
                cookie_installed = True
            elif 'jquery.tagcloud' in js_id.lower():
                jtagcloud_installed = True
            elif 'jquery.ajaxfileupload' in js_id.lower():
                jfileupload_installed = True
            #XXX This conflicts with Plone3 default jquery 1.2.x version
            #elif 'jquery' in js_id.lower():
                #jquery_installed = True
            if jquery_installed and ui_installed and \
               jfileupload_installed and \
               cookie_installed and jtagcloud_installed:
                break

        if not jquery_installed:
            res.append('++resource++jquery-1.3.2.js')
        if not ui_installed:
            res.append('++resource++jquery.ui-1.7.js')
        if not cookie_installed:
            res.append('++resource++jquery.cookie.js')
        if not jtagcloud_installed:
            res.append('++resource++jquery.tagcloud.js')
        if not jfileupload_installed:
            res.append('++resource++jquery.ajaxfileupload.js')

        res.append('++resource++eea.faceted-navigation-edit.js')
        res.append('++resource++eea.faceted-navigation-expand.js')
        return res

    @property
    def resources(self):
        """ Return edit resources
        """
        res = self.helper_js
        res.extend(self.js_libs)

        info = getUtility(IWidgetsInfo).widgets
        for widget in info.values():
            edit_js = widget.edit_js
            if isinstance(edit_js, tuple):
                res.extend(edit_js)
            else:
                res.append(edit_js)
        return res

    def __call__(self, *args, **kwargs):
        """ edit.js
        """
        self.request.RESPONSE.setHeader('content-type', 'text/javascript')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control', 'max-age=%d' % self.duration)
        return self.get_content()
