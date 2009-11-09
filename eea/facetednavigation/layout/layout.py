""" Layout adapters
"""
from zope import interface
from zope.component import getUtility
from persistent.list import PersistentList
from p4a.subtyper import interfaces as p4aifaces
try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.interfaces import IAnnotations

from interfaces import IFacetedLayout
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
        return IAnnotations(self.context).get(ANNO_FACETED_LAYOUT, 'folder_summary_view')

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

    def get_macro(self, template_id=None, macro='listing'):
        """ Get macro from layout
        """
        # Get default
        if not template_id:
            template_id = self.layout
        template = getattr(self.context, template_id, None)
        if not template:
            return None
        return template.macros.get(macro)

    @property
    def default_layouts(self):
        """ Get container default layouts
        """
        subtyper = getUtility(p4aifaces.ISubtyper)
        existing = subtyper.existing_type(self.context)

        if not existing:
            return self.context.getAvailableLayouts()
        return [('folder_summary_view', 'Default View')]
    #
    # Setters
    #
    def update_layout(self, layout=None):
        """ Save layout for context. Returns error if any.
        """
        if not layout:
            return 'Empty layout'
        if layout not in [x for x, y in self.layouts]:
            return 'Invalid layout id'

        IAnnotations(self.context)[ANNO_FACETED_LAYOUT] = layout
        return ''

    def update_layouts(self, layouts=None):
        """ Update layouts from given layouts. If not provided get layouts from
        context
        """
        if not layouts:
            layouts = self.default_layouts
        IAnnotations(self.context)[ANNO_FACETED_LAYOUTS]= PersistentList(layouts)
