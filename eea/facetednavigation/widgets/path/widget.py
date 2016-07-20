""" Path widget
"""
import logging
from Products.CMFPlone.utils import safeToInt

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.path.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.path.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.path.interfaces import DisplaySchemata
from eea.facetednavigation import EEAMessageFactory as _

logger = logging.getLogger('eea.facetednavigation.widgets.path')


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'path'
    widget_label = _('Path')

    groups = (DefaultSchemata, LayoutSchemata, DisplaySchemata)
    index = ViewPageTemplateFile('widget.pt')

    @property
    def data_root(self):
        """ Get navigation root
        """
        site = self.context.portal_url.getPortalObject()
        site_url = '/'.join(site.getPhysicalPath())
        site_url = site_url.strip('/')
        data_root = self.data.get('root', '') or ''
        data_root = data_root.strip().strip('/')
        if isinstance(data_root, unicode):
            data_root = data_root.encode('utf-8')
        if data_root.startswith(site_url):
            data_root = '/' + data_root
            return data_root.split('/')

        site_url = site_url.split('/')
        if data_root:
            data_root = data_root.split('/')
        else:
            data_root = []
        site_url.extend(data_root)
        site_url.insert(0, '')
        return site_url

    @property
    def root(self):
        """ Get navigation root language dependent
        """
        getLanguage = getattr(self.context, 'getLanguage', None)
        if not getLanguage:
            return self.data_root

        lang = getLanguage() or self.request.get('LANGUAGE', '')
        if not lang:
            return self.data_root

        root = '/'.join(self.data_root)
        root = self.context.unrestrictedTraverse(root, None)
        getTranslation = getattr(root, 'getTranslation', None)
        if not getTranslation:
            return self.data_root

        translation = getTranslation(lang)
        if not translation:
            return self.data_root

        url = translation.getPhysicalPath()
        return list(url)

    @property
    def default(self):
        """ Default value
        """
        data_default = self.data.get('default', '')
        if not data_default:
            return ''

        if isinstance(data_default, unicode):
            data_default = data_default.encode('utf-8')

        data_list = [d for d in data_default.strip().strip('/').split('/') if d]
        root = self.data_root[:]
        root.extend(data_list)

        url = '/'.join(root)
        folder = self.context.unrestrictedTraverse(url, None)
        if not folder:
            return ''

        getTranslation = getattr(folder, 'getTranslation', None)
        if not getTranslation:
            return data_default

        getLanguage = getattr(self.context, 'getLanguage', None)
        if not getLanguage:
            return data_default

        lang = getLanguage() or self.request.get('LANGUAGE', '')
        if not lang:
            return data_default

        translation = getTranslation(lang)
        if not translation:
            return data_default

        url = '/'.join(translation.getPhysicalPath())
        root = '/'.join(self.root)
        return url.replace(root, '', 1)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        value = value.strip().strip('/')
        if not value:
            return query

        url = self.root[:]
        if not url:
            return query

        url.extend(value.split('/'))
        value = '/'.join(url).rstrip('/')

        depth = safeToInt(self.data.get('depth', 0))
        query[index] = {"query": value, 'level': depth}

        logger.debug(query)
        return query
