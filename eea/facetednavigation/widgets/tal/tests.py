""" Doc tests
"""
import doctest
import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from eea.facetednavigation.tests.base import FacetedFunctionalTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    return unittest.TestSuite((
        Suite('widgets/tal/widget.txt',
              optionflags=OPTIONFLAGS,
              package='eea.facetednavigation',
              test_class=FacetedFunctionalTestCase),
    ))
