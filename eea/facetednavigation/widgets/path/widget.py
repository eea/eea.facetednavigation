""" Path widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from eea.facetednavigation.widgets.field import StringField

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        default='path',
        vocabulary_factory='eea.faceted.vocabularies.PathCatalogIndexes',
        widget=SelectionWidget(
            format='select',
            label='Catalog index',
            label_msgid='faceted_criteria_index',
            description='Catalog index to use for search',
            description_msgid='help_faceted_criteria_index',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default path to search in',
            description_msgid='help_faceted_criteria_path_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('root',
        schemata="default",
        widget=StringWidget(
            size=25,
            label='Root folder',
            label_msgid='faceted_criteria_path_root',
            description=('Navigation js-tree starting point '
                         '(relative to plone site. ex: SITE/data-and-maps)'),
            description_msgid='help_faceted_criteria_path_root',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('theme',
        schemata="display",
        default='green',
        vocabulary_factory='eea.faceted.vocabularies.JsTreeThemes',
        widget=SelectionWidget(
            format='select',
            label='Navigation tree theme',
            label_msgid='faceted_criteria_path_theme',
            description='Theme to be used with this widget',
            description_msgid='help_faceted_criteria_path_theme',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'path'
    widget_label = 'Path'
    view_js = (
        '++resource++jquery.jstree/jquery.tree.js',
        '++resource++eea.facetednavigation.widgets.path.tree.js',
        '++resource++eea.facetednavigation.widgets.path.view.js',
    )
    edit_js = (
        '++resource++jquery.jstree/jquery.tree.js',
        '++resource++eea.facetednavigation.widgets.path.tree.js',
        '++resource++eea.facetednavigation.widgets.path.edit.js',
    )
    view_css = '++resource++eea.facetednavigation.widgets.path.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.path.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'Search in'

    @property
    def root(self):
        """ Get navigation root
        """
        site_url = self.context.portal_url(1)
        data_root = self.data.get('root', '').strip().strip('/')
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

        value = value.strip().strip('/').split('/')

        url = self.root[:]
        url.extend(value)

        value = '/'.join(url)
        if not value:
            return query

        query[index] = {"query": value, 'level': 0}
        return query
