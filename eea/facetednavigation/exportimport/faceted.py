""" Faceted
"""
import logging
from zope.component import queryMultiAdapter
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.utils import XMLAdapterBase
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import ICriteria
logger = logging.getLogger('eea.facetednavigation.exportimport.faceted')

class FacetedNavigableXMLAdapter(XMLAdapterBase):
    """ GenericSetup XML Adapter for faceted navigable context
    """
    __used_for__ = IFacetedNavigable

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        criteria = ICriteria(self.context)
        exporter = queryMultiAdapter((criteria, self.environ), IBody)
        node.appendChild(exporter.node)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        criteria = ICriteria(self.context)
        for child in node.childNodes:
            if child.nodeName != 'criteria':
                continue
            importer = queryMultiAdapter((criteria, self.environ), IBody)
            importer.node = child

    node = property(_exportNode, _importNode)
