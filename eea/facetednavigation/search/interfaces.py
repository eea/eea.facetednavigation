from zope.interface import Interface

class IFacetedCatalog(Interface):
    """ Return portal catalog adapted with IReportCatalog depending if eea.reports
    is present or not.
    """
    def __call__(context, query):
        """ Call appropriate catalog
        """
