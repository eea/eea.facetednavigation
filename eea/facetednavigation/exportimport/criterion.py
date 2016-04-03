""" Criterion
"""
import logging
from zope.component import getUtility
from Products.GenericSetup.utils import XMLAdapterBase
from eea.facetednavigation.widgets.interfaces import ICriterion
from eea.facetednavigation.interfaces import IWidgetsInfo

logger = logging.getLogger('eea.facetednavigation.exportimport.criterion')

class CriterionXMLAdapter(XMLAdapterBase):
    """ GenericSetup XML Adapter for faceted criterion
    """
    __used_for__ = ICriterion

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        #self._doc = doc
        node = self._doc.createElement('criterion')
        node.setAttribute('name', self.context.getId())
        info = getUtility(IWidgetsInfo)
        widget_id = self.context.get('widget')
        widget = info(widget_id)

        properties = ['widget']
        properties.extend(widget.edit_schema.keys())
        for key in properties:
            value = self.context.get(key, None)
            if value is None:
                continue
            prop = self._doc.createElement('property')
            prop.setAttribute('name', key)
            if isinstance(value, (tuple, list)):
                for item in value:
                    if not value:
                        continue
                    element = self._doc.createElement('element')
                    element.setAttribute('value', item)
                    prop.appendChild(element)
            else:
                if isinstance(value, (int, bool)):
                    value = str(int(value))
                elif not isinstance(value, basestring):
                    value = str(value)
                child = self._doc.createTextNode(value)
                prop.appendChild(child)
            node.appendChild(prop)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        properties = {}
        for child in node.childNodes:
            if child.nodeName != 'property':
                continue

            key = child.getAttribute('name').encode('utf-8')
            elements = []
            for element in child.childNodes:
                if element.nodeName != 'element':
                    continue
                elements.append(element.getAttribute('value').encode('utf-8'))

            if elements:
                properties[key] = elements
            else:
                properties[key] = self._getNodeText(child).encode('utf-8')
        self.environ._tool.edit(self.context.getId(), **properties)

    node = property(_exportNode, _importNode)
