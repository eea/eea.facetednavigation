""" Various setup
"""
from plone25 import setupVarious as plone_setup

def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eeafacetednavigation.txt') is None:
        return

    plone_setup(context)
