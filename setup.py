""" EEA Faceted Navigation Installer
"""
from setuptools import setup, find_packages
import os
from os.path import join

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
          "Programming Language :: Zope",
          "Programming Language :: Python",
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
          'eea.faceted.vocabularies > 4.9',
          'collective.js.jqueryui',
          'eea.jquery',
          'Products.PloneTestCase',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
