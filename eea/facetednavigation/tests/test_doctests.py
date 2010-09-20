""" Doc tests
"""
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from base import FacetedFunctionalTestCase, LINGUAPLONE

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)



def test_suite():
    """ Suite
    """
    tests = unittest.TestSuite((
            Suite('README.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/facetednavigation.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/widgets.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/criteria.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/counter.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/exportimport.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/syndication.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/wrapper.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/versions.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/unicode.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
            Suite('docs/browser.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.facetednavigation',
                  test_class=FacetedFunctionalTestCase) ,
    ))
    #
    # LinguaPlone releted tests
    #
    if LINGUAPLONE:
        tests.addTest(Suite('docs/syncronize.txt',
                            optionflags=OPTIONFLAGS,
                            package='eea.facetednavigation',
                            test_class=FacetedFunctionalTestCase))
        tests.addTest(Suite('docs/language.txt',
                            optionflags=OPTIONFLAGS,
                            package='eea.facetednavigation',
                            test_class=FacetedFunctionalTestCase))
    return tests
