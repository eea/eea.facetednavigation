""" Proxy caching (squid, etc)
"""
from hashlib import md5
import cPickle
import logging
from zope.component import queryAdapter
from zope.interface import implements
from Products.Five.browser import BrowserView
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.versions.interfaces import IFacetedVersion
from eea.facetednavigation.config import ANNO_FACETED_VERSION
from zope.annotation.interfaces import IAnnotations

logger = logging.getLogger('eea.facetednavigation.cache.proxy')

class FacetedVersion(BrowserView):
    """ Generate a unique key to be added to faceted query/counter in order to
    invalidate cached urls when faceted settings are changed.
    """
    implements(IFacetedVersion)
    #
    # Private
    #
    def _digest(self):
        """ Compute a unique key from hidden faceted widgets.
        """
        config = queryAdapter(self.context, ICriteria)
        if not config:
            logger.exception('No ICriteria adapter found for %s', self.context)
            return ''

        query = {}
        criteria = config.values()
        for criterion in criteria:
            cid = criterion.getId()
            operator = criterion.get('operator', '')
            if operator:
                query.setdefault('%s-operator' % cid, operator)

            if not criterion.hidden:
                continue

            value = criterion.get('default', '')
            if not value or value in ['All', 'all', u'All', u'all']:
                continue

            query[cid] = value

        if not query:
            return ''

        return md5(cPickle.dumps(query)).hexdigest()

    def _set(self, value=None):
        """ Set version key
        """
        key = self._digest()
        if key == self.key:
            return key

        anno = IAnnotations(self.context)
        anno[ANNO_FACETED_VERSION] = key
        return key

    def _get(self):
        """ Get version key
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_FACETED_VERSION, '')
    #
    # Public interface
    #
    key = property(_get, _set)

    def __call__(self, **kwargs):
        return self.key
