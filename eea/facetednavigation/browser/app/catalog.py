""" Faceted catalog views
"""
import json
import logging
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from eea.facetednavigation.caching import ramcache
logger = logging.getLogger('eea.facetednavigation.browser.catalog')

def cacheKey(method, self, *args, **kwargs):
    """ Generate unique cache id for faceted catalog indexes types
    """
    form = getattr(self.request, 'form', {})
    return form

class FacetedCatalog(BrowserView):
    """ Render an error message when something is wrong with widgets
    """
    def types(self, **kwargs):
        """ Return a mapping between catalog indexes and types
        """
        ctool = getToolByName(self.context, 'portal_catalog')
        indexes = ctool.getIndexObjects()
        res = {}
        for index in indexes:
            operator = 'operator' in getattr(index, 'query_options', [])
            res[index.getId()] = {
                'metatype': index.meta_type,
                'operator': operator and ['or', 'and'] or ['or']
            }
        return res

    @ramcache(cacheKey, dependencies=['eea.facetednavigation'])
    def json_types(self, **kwargs):
        """ Return catalog indexes, types mapping as json object
        """
        if self.request:
            kwargs.update(self.request.form)
            self.request.response.setHeader('Content-Type',
                                            'application/json; charset=utf-8')

        return json.dumps(self.types(**kwargs))
