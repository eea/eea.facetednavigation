""" Faceted global settings
"""

from zope.interface import Interface

class IHidePloneLeftColumn(Interface):
    """ Marker interface to hide plone default left column in
        facetednavigation view
    """

class IHidePloneRightColumn(Interface):
    """ Marker interface to hide plone default right column in
        facetednavigation view
    """

class ISettingsHandler(Interface):
    """ Edit faceted global settings
    """
    def hide_left_column():
        """ Hide plone default left column in facetednavigation view
        """

    def hide_right_column():
        """ Hide plone default right column in facetednavigation view
        """
