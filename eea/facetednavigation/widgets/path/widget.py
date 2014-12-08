""" Path widget
"""
import logging
from Products.CMFPlone.utils import safeToInt
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _

logger = logging.getLogger('eea.facetednavigation.widgets.path')

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        default='path',
        vocabulary_factory='eea.faceted.vocabularies.PathCatalogIndexes',
        widget=SelectionWidget(
            format='select',
            label=_(u'Catalog index'),
            description=_(u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    StringField('root',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_(u'Root folder'),
            description=_(u'Navigation js-tree starting point '
                        u'(relative to plone site. ex: SITE/data-and-maps)'),
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_(u'Default value'),
            description=_(u"Default path to search in (relative to "
                           "root folder)"),
            i18n_domain="eea"
        )
    ),
    StringField('depth',
        schemata="default",
        default=0,
        widget=StringWidget(
            size=25,
            label=_(u'Search Depth'),
            description=_(u'Depth to search the path. 0=this level, '
                        u'-1=all subfolders recursive, and any other positive '
                        u'integer count the subfolder-levels to search.'),
            i18n_domain="eea"
        )
    ),
    StringField('theme',
        schemata="display",
        default='green',
        vocabulary_factory='eea.faceted.vocabularies.JsTreeThemes',
        widget=SelectionWidget(
            format='select',
            label=_(u'Navigation tree theme'),
            description=_(u'Theme to be used with this widget'),
            i18n_domain="eea"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'path'
    widget_label = _('Path')
    view_js = (
        '++resource++eea.facetednavigation.widgets.path.tree.js',
        '++resource++eea.facetednavigation.widgets.path.view.js',
    )
    edit_js = (
        '++resource++eea.facetednavigation.widgets.path.tree.js',
        '++resource++eea.facetednavigation.widgets.path.edit.js',
    )
    view_css = '++resource++eea.facetednavigation.widgets.path.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.path.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'Search in'

    @property
    def data_root(self):
        """ Get navigation root
        """
        site = self.context.portal_url.getPortalObject()
        site_url = '/'.join(site.getPhysicalPath())
        site_url = site_url.strip('/')
        data_root = self.data.get('root', '').strip().strip('/')
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
