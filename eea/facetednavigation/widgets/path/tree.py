""" JsTree views
"""
import simplejson as json
from zope.component import queryAdapter

from Products.Five.browser import BrowserView
from Products.CMFPlone.browser.navtree import buildFolderTree
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.CMFCore.utils import getToolByName

from eea.facetednavigation.interfaces import ICriteria

class FacetedTree(BrowserView):
    """ Create jstree response used by faceted path widget
    """
    def __init__(self, context, request):
        super(FacetedTree, self).__init__(context, request)
        self.rootPath = ''

    def navigationTreeRootPath(self):
        """ Used by NavigationStrategy
        """
        return self.rootPath

    def get_root(self, cid):
        """ Get root from faceted widget
        """
        criteria = queryAdapter(self.context, ICriteria)
        if not criteria:
            return ''

        criterion = criteria.get(cid)
        widget = criteria.widget(cid=cid)
        widget = widget(self.context, self.request, criterion)
        return widget.root[:]

    def tree(self, **kwargs):
        """ Get nodes
        """
        cid = kwargs.get('cid', None)
        if not cid:
            return []

        root = self.get_root(cid)
        if not root:
            return []

        path = kwargs.get('path', '').strip().strip('/')
        if path:
            path = path.split('/')
        else:
            path = []

        url = root[:]
        url.extend(path)
        url = '/'.join(url)

        query = {
            'path': {'query': url, 'depth': 2},
            # TODO
            #'portal_type': ['Folder'],
            #'Language': 'en',
            # 'review_state': 'published'
        }

        self.rootPath = url

        if isinstance(url, unicode):
            url = url.encode('utf-8')
        obj = self.context.unrestrictedTraverse(url.strip('/'), self.context)
        strategy = FacetedTreeStrategy(obj, self)
        data = buildFolderTree(self.context, obj=obj, query=query,
                               strategy=strategy)

        children = data['children']
        nodes = []
        for node in children:
            node_url = node['path']
            node_url = node_url.replace('/'.join(root), '', 1)
            node_id = cid + node_url.replace('/', '-')

            node_children = node.get('children', [])
            node_children = [n for n in node_children if strategy.nodeFilter(n)]
            node_state = len(node_children) and 'closed' or 'leaf'

            nodes.append({
                'attributes': {
                    'id': node_id,
                    'path': node_url
                },
                'data': {
                    'title': node.get('Title', 'Missing title'),
                },
                'state': node_state
            })
        return nodes

    def breadcrumbs(self, **kwargs):
        """ Create custom breadcrumbs
        """
        cid = kwargs.get('cid', None)
        if not cid:
            return []

        root = self.get_root(cid)
        if not root:
            return []

        path = kwargs.get('path', '').strip().strip('/')
        if path:
            path = path.split('/')
        else:
            path = []
        if not path:
            return []

        ctool = getToolByName(self.context, 'portal_catalog')
        res = []
        url = root[:]
        breadcrumb_path = ['']
        for breadcrumb in path:
            url.append(breadcrumb)
            breadcrumb_path.append(breadcrumb)

            breadcrumb_url = '/'.join(url)
            query = {'query': breadcrumb_url, 'depth': 0}
            brains = ctool(path=query)
            if not brains:
                continue
            brain = brains[0]
            res.append({
                'url': '/'.join(breadcrumb_path),
                'title': brain.Title
            })
        return res
    #
    # JSON
    #
    def json_tree(self, **kwargs):
        """ Get navigation tree as json
        """
        if self.request:
            kwargs.update(self.request.form)
        return json.dumps(self.tree(**kwargs))

    def json_breadcrumbs(self, **kwargs):
        """ Get breadcrumbs as json
        """
        if self.request:
            kwargs.update(self.request.form)
        return json.dumps(self.breadcrumbs(**kwargs))

class FacetedTreeStrategy(DefaultNavtreeStrategy):
    """ Custom strategy
    """
    def nodeFilter(self, node):
        if not getattr(node['item'], 'is_folderish', False):
            return False
        return DefaultNavtreeStrategy.nodeFilter(self, node)
