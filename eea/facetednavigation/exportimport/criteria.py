""" Criteria
"""
import logging
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.component import queryMultiAdapter
from zope.interface import implements
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.utils import XMLAdapterBase
from eea.facetednavigation.interfaces import IFacetedNavigable
from Products.GenericSetup.context import BaseContext
from Products.GenericSetup.interfaces import ISetupEnviron
logger = logging.getLogger('eea.facetednavigation.exportimport.criteria')

class CriteriaContext(BaseContext):
    """ Criteria import environ
    """
    implements(ISetupEnviron)

    def __init__(self, tool, encoding='utf-8'):
        self._tool = tool
        self._site = aq_parent( aq_inner( tool.context ) )
        self._loggers = {}
        self._messages = []
        self._encoding = encoding
        self._should_purge = True

class CriteriaXMLAdapter(XMLAdapterBase):
    """ GenericSetup XML Adapter for faceted criteria
    """
    __used_for__ = IFacetedNavigable

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        env = CriteriaContext(self.context)
        node = self._doc.createElement('criteria')
        for criterion in self.context.values():
            exporter = queryMultiAdapter((criterion, env), IBody)
            node.appendChild(exporter.node)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        env = CriteriaContext(self.context)
        should_purge = env.shouldPurge()
        if should_purge:
            cids = self.context.keys()
            for cid in cids:
                self.context.delete(cid)

        for child in node.childNodes:
            if child.nodeName != 'criterion':
                continue

            name = child.getAttribute('name')

            cid = self.context.add('text', 'top', _cid_=name)
            criterion = self.context.get(cid)

            importer = queryMultiAdapter((criterion, env), IBody)
            importer.node = child

    node = property(_exportNode, _importNode)
