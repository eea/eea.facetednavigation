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
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
      ],
      keywords='EEA Faceted Navigation FacetedNavigation Add-on Add-ons Plone Zope',
      author='European Environment Agency: IDM2 A-Team',
      author_email="eea-edw-a-team-alerts@googlegroups.com",
      url='http://github.com/collective/eea.facetednavigation',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'eea.faceted.vocabularies > 5.9',
          'collective.js.jqueryui',
          'eea.jquery > 9.1',
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
