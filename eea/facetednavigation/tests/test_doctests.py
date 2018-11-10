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

import re
import six


OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", want)
            got = re.sub(' encoding="utf-8"', '', want)
            # want = re.sub("b'(.*?)'", "'\\1'", want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    """ Suite
    """
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'README.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/facetednavigation.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/widgets.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/criteria.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/counter.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/exportimport.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/solr.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/syndication.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/wrapper.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/versions.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/unicode.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/browser.txt',
                optionflags=OPTIONFLAGS,
                checker=Py23DocChecker(),
                package='eea.facetednavigation'),
            layer=FUNCTIONAL_TESTING),
    ])

    if LinguaPlone:
        suite.addTests([
            layered(
                doctest.DocFileSuite(
                    'docs/syncronize.txt',
                    optionflags=OPTIONFLAGS,
                    checker=Py23DocChecker(),
                    package='eea.facetednavigation'),
                layer=FUNCTIONAL_TESTING),
            layered(
                doctest.DocFileSuite(
                    'docs/language.txt',
                    optionflags=OPTIONFLAGS,
                    checker=Py23DocChecker(),
                    package='eea.facetednavigation'),
                layer=FUNCTIONAL_TESTING),
        ])

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
