""" Various setup
"""
def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eeafacetednavigation.txt') is None:
        return
