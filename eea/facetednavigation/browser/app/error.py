""" Errors
"""
import logging
from pprint import pformat
from zope.component import queryAdapter
from eea.facetednavigation.interfaces import ICriteria
from Products.Five.browser import BrowserView

logger = logging.getLogger('eea.facetednavigation.browser.error')

class FacetedError(BrowserView):
    """ Render an error message when something is wrong with widgets
    """
    def __call__(self, **kwargs):
        error = kwargs.get('error', None)
        res = {
            'type': getattr(error, 'type', ''),
            'value': getattr(error, 'value', '')
        }
        cid = kwargs.get('cid', '')
        msg = ''
        if cid:
            criteria = queryAdapter(self.context, ICriteria)
            if criteria:
                data = criteria.get(cid)
                if data:
                    msg = pformat(data.__dict__)


        logger.exception('\n%s\n', msg)
        return self.index(error=res)
