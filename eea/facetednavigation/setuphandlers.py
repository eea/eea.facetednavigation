""" Various setup
"""
from eea.facetednavigation.config import ANNO_CRITERIA
from eea.facetednavigation.interfaces import IDisableSmartFacets
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import IFacetedSearchMode
from eea.facetednavigation.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.interfaces import IHidePloneRightColumn
from eea.facetednavigation.settings.interfaces import IDontInheritConfiguration
from logging import getLogger
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import noLongerProvides


log = getLogger("eea.facetednavigation.post_uninstall")


@implementer(INonInstallable)
class HiddenProfiles(object):
    """Hidden profiles"""

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            "eea.facetednavigation:uninstall",
        ]


def setupVarious(context):
    """Do some various setup."""
    if context.readDataFile("eea.facetednavigation.txt") is None:
        return


def uninstall_faceted(context):
    """Custom script to remove interface traces on uninstall"""
    remove_annotations(context)
    remove_default_views(context)
    remove_assigned_interfaces(context)


def remove_assigned_interfaces(context):
    remove_interface(context, IFacetedNavigable)
    remove_interface(context, IDisableSmartFacets)
    remove_interface(context, IHidePloneLeftColumn)
    remove_interface(context, IHidePloneRightColumn)
    remove_interface(context, IFacetedSearchMode)
    remove_interface(context, IDontInheritConfiguration)


def remove_interface(context, iface):
    """Remove interface assignment from objects"""
    portal_catalog = getToolByName(context, "portal_catalog")
    brains = portal_catalog(object_provides=iface.__identifier__)
    log.info(
        "Removing {0} interface from {1} objects".format(
            iface.__identifier__, len(brains)
        )
    )
    for brain in brains:
        item = brain.getObject()
        noLongerProvides(item, iface)


def remove_annotations(context):
    """Remove criteria configuration from annotations"""
    portal_catalog = getToolByName(context, "portal_catalog")
    brains = portal_catalog(object_provides=IFacetedNavigable.__identifier__)
    for brain in brains:
        item = brain.getObject()
        annotations = IAnnotations(item)
        if ANNO_CRITERIA in annotations:
            del annotations[ANNO_CRITERIA]
            log.info("Removed criteria configuration from {0}".format(brain.getPath()))


def remove_default_views(context):
    portal_catalog = getToolByName(context, "portal_catalog")
    brains = portal_catalog(object_provides=IFacetedNavigable.__identifier__)
    for brain in brains:
        item = brain.getObject()
        if (
            item.hasProperty("layout")
            and item.getProperty("layout") == "facetednavigation_view"
        ):
            item.manage_delProperties(["layout"])
            log.info(
                "Removed facetednavigation_view layout from {0}".format(brain.getPath())
            )
