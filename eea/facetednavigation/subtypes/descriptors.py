from zope import interface
from interfaces import IFacetedNavigable
from p4a.subtyper.interfaces import IPortalTypedFolderishDescriptor

class FacetedNavigableDescriptor(object):
    """ Abstract report descriptor
    """
    interface.implements(IPortalTypedFolderishDescriptor)
    title = u'Faceted Navigable'
    description = u'Faceted navigable'
    type_interface = IFacetedNavigable

class FolderFacetedNavigableDescriptor(FacetedNavigableDescriptor):
    """ Folder descriptor
    """
    for_portal_type = 'Folder'

class LargeFolderFacetedNavigableDescriptor(FacetedNavigableDescriptor):
    """ Large Folder descriptor
    """
    for_portal_type = 'Large Plone Folder'

class TopicFacetedNavigableDescriptor(FacetedNavigableDescriptor):
    """ Folder descriptor
    """
    for_portal_type = 'Topic'

class RichTopicNavigableDescriptor(FacetedNavigableDescriptor):
    """ RichTopic descriptor
    """
    for_portal_type = 'RichTopic'
