""" Faceted layout event handlers
"""
from zope.component import queryAdapter, queryMultiAdapter
from eea.facetednavigation.interfaces import ICriteria
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.context import SnapshotImportContext

def faceted_will_be_enabled(doc, evt):
    """ EVENT: faceted navigation is going to be enabled
    """
    return

def faceted_enabled(doc, evt):
    """ EVENT: faceted navigation enabled
    """
    # Set default view
    if hasattr(doc, 'setLayout'):
        doc.setLayout('facetednavigation_view')

    # Add default widgets
    add_default_widgets(doc)

    # Reindex
    doc.reindexObject(['object_provides', ])

def faceted_disabled(doc, evt):
    """ EVENT: faceted navigation disabled
    """
    if doc.hasProperty('layout'):
        doc.manage_delProperties(['layout'])

    # Reindex
    doc.reindexObject(['object_provides', ])

def add_default_widgets(context):
    """ Add default widgets to context
    """
    criteria = queryAdapter(context, ICriteria)
    if not criteria:
        return

    # Configure widgets only for canonical (LinguaPlone only)
    getCanonical = getattr(context, 'getCanonical', None)
    if getCanonical:
        canonical = getCanonical()
        if context != canonical:
            return

    # Criteria already changed, we don't want to mess them
    if criteria.keys():
        return

    widgets = context.unrestrictedTraverse('@@default_widgets.xml')
    if not widgets:
        return

    xml = widgets()
    environ = SnapshotImportContext(context, 'utf-8')
    importer = queryMultiAdapter((context, environ), IBody)
    if not importer:
        return
    importer.body = xml
