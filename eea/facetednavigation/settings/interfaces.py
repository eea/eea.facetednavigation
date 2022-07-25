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

class IDisableSmartFacets(Interface):
    """ Marker interface to always show facets even if there are not enough
        results
    """

class IInheritConfiguration(Interface):
    """ Marker interface to prevent inheriting configuration from the
        canonical language
    """

class IDontInheritConfiguration(Interface):
    """ Marker interface to prevent inheriting configuration from the
        canonical language
    """

class ISettingsHandler(Interface):
    """ Edit faceted global settings
    """
    def toggle_left_column():
        """ Show / hide plone default left column in facetednavigation view
        """

    def toggle_right_column():
        """ Show / hide plone default right column in facetednavigation view
        """

    def toggle_smart_facets():
        """ Enable / disable 'smart facets hiding' in facetednavigation view
        """

    def toggle_inherit_config():
        """ Enable / disable 'Inherit configuration from canonical language' in
            facetednavigation view
        """
