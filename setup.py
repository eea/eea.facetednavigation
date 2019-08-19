""" EEA Faceted Navigation Installer
"""
import os
from os.path import join
from setuptools import setup, find_packages

NAME = 'eea.facetednavigation'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="EEA Faceted Navigation",
      long_description_content_type="text/x-rst",
      long_description=(
          open("README.rst").read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      # https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope",
          "Framework :: Zope2",
          "Framework :: Zope :: 2",
          "Framework :: Zope :: 4",
          "Framework :: Plone",
          "Framework :: Plone :: Addon",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Framework :: Plone :: 5.2",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA Faceted Navigation FacetedNavigation Add-ons Plone Zope',
      author='European Environment Agency: IDM2 A-Team',
      author_email='eea-edw-a-team-alerts@googlegroups.com',
      url='https://github.com/collective/eea.facetednavigation',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'eea.faceted.vocabularies > 6.0',
          'collective.js.jqueryui',
          'eea.jquery > 10.2',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
