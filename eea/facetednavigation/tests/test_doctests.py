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
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'README.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/facetednavigation.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/widgets.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/criteria.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/counter.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/exportimport.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/solr.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/syndication.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/wrapper.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/versions.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/unicode.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/browser.txt',
                optionflags=OPTIONFLAGS,
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
    ])

    if LinguaPlone:
        suite.addTests([
            layered(
                doctest.DocFileSuite(
                    'docs/syncronize.txt',
                    optionflags=OPTIONFLAGS,
                    package='eea.facetednavigation'),
                layer=FUNCTIONAL_TESTING),
            layered(
                doctest.DocFileSuite(
                    'docs/language.txt',
                    optionflags=OPTIONFLAGS,
                    package='eea.facetednavigation'),
                layer=FUNCTIONAL_TESTING),
        ])

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
