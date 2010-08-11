""" Doc tests
"""
import doctest
import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from eea.facetednavigation.tests.base import FacetedFunctionalTestCase
from eea.facetednavigation.tests.base import LINGUAPLONE

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    if LINGUAPLONE:
        return unittest.TestSuite((
            Suite('widgets/path/widget.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('widgets/path/tree.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
        ))
    return unittest.TestSuite()
