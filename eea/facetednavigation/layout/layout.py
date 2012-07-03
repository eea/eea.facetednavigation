""" Layout adapters
"""
from zope import interface
from zope.component import getUtility, queryMultiAdapter
from zope.annotation.interfaces import IAnnotations
from eea.facetednavigation.interfaces import IViewsInfo
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.config import ANNO_FACETED_LAYOUT

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
            ANNO_FACETED_LAYOUT, 'faceted-preview-items')

    @property
    def layouts(self):
        """ Available layouts
        """
        layouts = self.default_layouts
        res = []
        for template_id, title in layouts:
            if not self.get_macro(template_id):
                continue
            res.append((template_id, title))

        # Dynamically registered faceted views
        info = getUtility(IViewsInfo)
        for view in info.keys():
            if not self.get_macro(view):
                continue
            res.append((view, info.label(view)))

        return res

    def get_macro(self, template_id=None, macro='content-core'):
        """ Get macro from layout
        """
        # Get default
        if not template_id:
            template_id = self.layout

        request = getattr(self.context, 'REQUEST', None)


        template = queryMultiAdapter((self.context, request), name=template_id)
        if template:
            # Zope3 view
            macros = getattr(template, 'macros', None)
            if not macros:
                index = getattr(template, 'index', None)
                macros = getattr(index, 'macros', None)
        else:
            # Zope2 skins template
            template = self.context.restrictedTraverse(template_id, None)
            macros = getattr(template, 'macros', None)

        if not macros:
            return None

        try:
            return macros[macro]
        except KeyError:
            return None

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

