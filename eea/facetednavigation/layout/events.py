""" Faceted layout event handlers
"""
from zope.component import queryAdapter, queryMultiAdapter
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.interfaces import ICriteria
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.context import SnapshotImportContext

def subtype_added(evt):
    """ EVENT: subtype added
    """
    # Layout
    doc = evt.object
    layout_adapter = queryAdapter(doc, IFacetedLayout)
    if not layout_adapter:
        return

    if doc.hasProperty('layout'):
        doc.manage_delProperties(['layout'])
    layout_adapter.update_layout('folder_summary_view')

    # Add default widgets
    add_default_widgets(doc)

def subtype_removed(evt):
    """ EVENT: subtype removed
    """
    doc = evt.object
    layout_adapter = queryAdapter(doc, IFacetedLayout)
    if not layout_adapter:
        return
    layout_adapter.update_layouts()

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
