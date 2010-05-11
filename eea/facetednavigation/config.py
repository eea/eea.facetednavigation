""" EEA faceted config variables
"""
ANNO_CRITERIA = 'FacetedCriteria'
ANNO_FACETED_LAYOUTS = 'FacetedLayouts'
ANNO_FACETED_LAYOUT = 'FacetedLayout'
ANNO_FACETED_VERSION = 'FacetedVersion'
try:
    import zope.annotation
except ImportError:
    PLONE = 2.5
else:
    PLONE = 3
