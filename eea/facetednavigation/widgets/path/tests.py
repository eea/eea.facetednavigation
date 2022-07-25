""" Doc tests
"""
import doctest
import unittest
from eea.facetednavigation.tests.base import FUNCTIONAL_TESTING
from plone.testing import layered
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
    suite = unittest.TestSuite()
    if not LinguaPlone:
        return suite

    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'widgets/path/widget.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'widgets/path/tree.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
    ])
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
