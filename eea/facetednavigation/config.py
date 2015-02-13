""" EEA faceted config variables
"""
ANNO_CRITERIA = 'FacetedCriteria'
ANNO_FACETED_LAYOUTS = 'FacetedLayouts'
ANNO_FACETED_LAYOUT = 'FacetedLayout'
ANNO_FACETED_VERSION = 'FacetedVersion'

import pkg_resources
try:
    pkg_resources.get_distribution('collective.solr')
except pkg_resources.DistributionNotFound:
    HAS_SOLR = False
else:
    HAS_SOLR = True
