""" Custom python logic for the Faceted Views
"""
from Products.Five.browser import BrowserView

class SummaryView(BrowserView):
    """ Example Faceted view for the results. You can skip the class attribute
    in the ZCML if you don't have custom logic for your view.

    The coolest thing of this is that you can re-filter the results by
    a custom logic, you can extend the search to external sites, display items
    on a map, or do whatever you want.
    This is limited only by your imagination... and your python skills :)
    """

    def truncate(self, text='', chars=100):
        """ Truncate text by given number of characters
        """
        if len(text) <= chars:
            return text
        return text[:chars] + '...'
