""" Browser interfaces
"""
from zope.interface import Interface

class IFacetedCriteriaHandler(Interface):
    """ Edit faceted criteria
    """
    def add():
        """ Add empty criterion
        """

    def edit():
        """ Update criteria properties
        """

    def delete(paths):
        """ Delete criteria by given paths (ids)
        """

    def __call__():
        """ Call handler with
        """

class IFacetedCriterionHandler(Interface):
    """ Edit faceted criterion in criteria
    """
    def add():
        """ Add a criterion with properties
        """

    def edit(cid):
        """ Edit criterion
        """

    def delete(cid):
        """ Delete criterion by given cid
        """

class IFacetedPositionHandler(Interface):
    """ Handle criteria positions
    """
    def update():
        """ Update position by given slots
        """

    def move_up():
        """ Move criterion up
        """

    def move_down():
        """ Move criterion down
        """

class IFacetedFormHandler(Interface):
    """ Handle criteria from a static form
    """
    def __call__():
        """ Run appropiate handler
        """

