""" Version related events
"""
import logging
from zope.component import queryMultiAdapter
from interfaces import IFacetedVersion
logger = logging.getLogger('eea.faceted.versions')

def updateFacetedVersion(obj, event):
    """ Generate new version for faceted configuration.
    """
    request = getattr(obj, 'request', None)
    version = queryMultiAdapter((obj, request), name=u'faceted_version')
    if not version:
        logger.exception('Could not update faceted version for %s', obj)
        return
    version.key = 'Generate another key'
