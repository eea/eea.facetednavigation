""" Doc tests
"""
import doctest
import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from eea.facetednavigation.tests.base import FacetedFunctionalTestCase
try:
    from Products import LinguaPlone
    LinguaPlone = True if LinguaPlone else False
except ImportError:
    LinguaPlone = False

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    if not LinguaPlone:
        return unittest.TestSuite()

    return unittest.TestSuite((
        Suite('widgets/path/widget.txt',
              optionflags=OPTIONFLAGS,
              package='eea.facetednavigation',
              test_class=FacetedFunctionalTestCase),
        Suite('widgets/path/tree.txt',
              optionflags=OPTIONFLAGS,
              package='eea.facetednavigation',
              test_class=FacetedFunctionalTestCase),
    ))
