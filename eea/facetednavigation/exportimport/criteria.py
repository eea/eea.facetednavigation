""" Criteria
"""
import logging
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.component import queryMultiAdapter
from zope.interface import implementer
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.context import BaseContext
from Products.GenericSetup.interfaces import ISetupEnviron
from eea.facetednavigation.interfaces import IFacetedNavigable

logger = logging.getLogger("eea.facetednavigation")


@implementer(ISetupEnviron)
class CriteriaContext(BaseContext):
    """Criteria import environ"""

    def __init__(self, tool, encoding="utf-8"):
        self._tool = tool
        self._site = aq_parent(aq_inner(tool.context))
        self._loggers = {}
        self._messages = []
        self._encoding = encoding
        self._should_purge = True


class CriteriaXMLAdapter(XMLAdapterBase):
    """GenericSetup XML Adapter for faceted criteria"""

    __used_for__ = IFacetedNavigable

    def _exportNode(self):
        """Export the object as a DOM node."""
        env = CriteriaContext(self.context)
        node = self._doc.createElement("criteria")
        for criterion in self.context.values():
            exporter = queryMultiAdapter((criterion, env), IBody)
            node.appendChild(exporter.node)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node."""
        env = CriteriaContext(self.context)
        should_purge = env.shouldPurge()
        if node.getAttribute("purge"):
            should_purge = self._convertToBoolean(node.getAttribute("purge"))
        if should_purge:
            cids = list(self.context.keys())
            for cid in cids:
                self.context.delete(cid)

        for child in node.childNodes:
            if child.nodeName != "criterion":
                continue

            name = child.getAttribute("name")
            # check if purge at criterion level if not already at criteria level
            if not should_purge and child.getAttribute("purge"):
                should_purge_child = self._convertToBoolean(child.getAttribute("purge"))
                if should_purge_child and name in list(self.context.keys()):
                    self.context.delete(name)
            try:
                # we need to find the 'position' and 'section' because
                # it is used to sort criteria when the criterion is added
                pos = [
                    s
                    for s in child.getElementsByTagName("property")
                    if s.getAttribute("name") == "position"
                ]
                position = pos[0].childNodes[0].nodeValue if pos else "top"
                sect = [
                    s
                    for s in child.getElementsByTagName("property")
                    if s.getAttribute("name") == "section"
                ]
                section = sect[0].childNodes[0].nodeValue if sect else "default"
                widget = [
                    w
                    for w in child.getElementsByTagName("property")
                    if w.getAttribute("name") == "widget"
                ]
                widget = widget[0].childNodes[0].nodeValue if widget else "text"
                cid = self.context.add(widget, position, section, _cid_=name)
            except KeyError:
                # element already exists, we log and we continue
                # this could be the case if should_purge is False
                logger.warning(
                    'Criterion with name "%s" could not be created '
                    'on "%s" because a criterion with same name '
                    "already exists!",
                    name,
                    "/".join(env._tool.context.getPhysicalPath()),
                )
                continue
            criterion = self.context.get(cid)

            importer = queryMultiAdapter((criterion, env), IBody)
            importer.node = child

    node = property(_exportNode, _importNode)
