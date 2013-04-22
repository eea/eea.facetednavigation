""" Layout interfaces
"""
from zope import interface

class ILayoutMenuHandler(interface.Interface):
    """ Faceted layout change handler
    """

class IFacetedLayout(interface.Interface):
    """ Utility to get available layouts, current layout.
    """

    layout = interface.Attribute("""Current layout""")
    layouts = interface.Attribute("""Available layouts""")
    default_layouts = interface.Attribute("""et container default layouts""")

    def get_macro(self, template_id=None, macro='content-core'):
        """ Get macro from layout
        """

    def update_layout(self, layout=None):
        """ Save layout for context. Returns error if any.
        """
