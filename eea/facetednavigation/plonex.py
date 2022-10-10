""" Plone X compatibility over time
"""
from zope.interface import Interface


#
# collective.solr
#

try:
    from collective.solr import exceptions
    from collective.solr import interfaces

    ISolrConnectionManager = interfaces.ISolrConnectionManager
    ISolrSearch = interfaces.ISearch

    SolrConnectionException = exceptions.SolrConnectionException
    SolrInactiveException = exceptions.SolrInactiveException

except (ImportError, AttributeError):

    class ISolrConnectionManager(Interface):
        """collective.solr not installed"""

    class ISolrSearch(Interface):
        """collective.solr not installed"""

    class SolrConnectionException:
        """collective.solr not installed"""

    class SolrInactiveException:
        """collective.solr not installed"""

    HAVE_SOLR = False
else:
    HAVE_SOLR = True
