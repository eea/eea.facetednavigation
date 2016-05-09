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
      long_description=(
          open("README.txt").read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
      ],
      keywords='eea faceted navigation',
      author='Alin Voinea, Alexandru Ghica, Antonio De Marinis',
      author_email='webadmin@eea.europa.eu',
      url='http://plone.org/products/eea.facetednavigation',
      license='MPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'eea.faceted.vocabularies > 5.2',
          'collective.js.jqueryui',
          'eea.jquery > 8.6',
          'Products.PloneTestCase',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
