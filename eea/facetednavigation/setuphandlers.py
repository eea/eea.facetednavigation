""" Various setup
"""
def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eea.facetednavigation.txt') is None:
        return
