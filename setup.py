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
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
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
          'eea.faceted.vocabularies',
          'collective.js.jqueryui',
          'eea.jquery',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
