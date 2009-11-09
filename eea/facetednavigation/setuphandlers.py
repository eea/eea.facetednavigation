from Products.CMFCore.utils import getToolByName

def addActionProvider(portal):
    """Add action providers.
    """
    atool = getToolByName(portal, 'portal_actions')
    if 'portal_fiveactions' not in atool.listActionProviders():
        atool.addActionProvider('portal_fiveactions')

def setupVarious(context):
    """ Do some various setup.
    """
    portal = context.getSite()

    # Plone 3 HACKS
    # Add action-provider as you can not add it in actions.xml because there is
    # a hardcoded _SPECIAL_PROVIDERS is XMLAdapter that filter them.
    addActionProvider(portal)
