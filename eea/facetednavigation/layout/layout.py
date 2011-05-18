""" Layout adapters
"""
from zope import interface
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.config import (
    ANNO_FACETED_LAYOUT,
    ANNO_FACETED_LAYOUTS,
)

class FacetedLayout(object):
    """ Faceted Layout
    """
    interface.implements(IFacetedLayout)

    def __init__(self, context):
        self.context = context
    #
    # Getters
    #
    @property
    def layout(self):
        """ Current layout
        """
        return IAnnotations(self.context).get(
            ANNO_FACETED_LAYOUT, 'folder_listing')

    @property
    def layouts(self):
        """ Available layouts
        """
        layouts = IAnnotations(self.context).get(ANNO_FACETED_LAYOUTS, [])
        res = []
        for template_id, title in layouts:
            if not self.get_macro(template_id):
                continue
            res.append((template_id, title))
        return res

    def get_macro(self, template_id=None, macro='content-core'):
        """ Get macro from layout
        """
        # Get default
        if not template_id:
            template_id = self.layout
        template = self.context.restrictedTraverse(template_id, None)
        if not hasattr(template, 'macros'):
            return None
        return template.macros.get(macro)

    @property
    def default_layouts(self):
        """ Get container default layouts
        """
        return self.context.getAvailableLayouts()
    #
    # Setters
    #
    def update_layout(self, layout=None):
        """ Save layout for context. Returns error if any.
        """
        if not layout:
            return 'Empty layout'
        if layout not in [x[0] for x in self.layouts]:
            return 'Invalid layout id'

        IAnnotations(self.context)[ANNO_FACETED_LAYOUT] = layout
        return ''

    def update_layouts(self, layouts=None):
        """ Update layouts from given layouts. If not provided get layouts from
        context
        """
        if not layouts:
            layouts = self.default_layouts
        IAnnotations(self.context)[
            ANNO_FACETED_LAYOUTS] = PersistentList(layouts)
