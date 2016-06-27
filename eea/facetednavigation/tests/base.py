""" Base test cases
"""
from plone.testing import z2
from plone.app.testing import TEST_USER_ID
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from Products.CMFPlone import setuphandlers
from plone.app.testing import setRoles
try:
    from Products import LinguaPlone
    LinguaPlone = True if LinguaPlone else False
except ImportError:
    LinguaPlone = False

class EEAFixture(PloneSandboxLayer):
    """ EEA Testing Policy
    """
    def setUpZope(self, app, configurationContext):
        """ Setup Zope
        """
        import eea.facetednavigation
        self.loadZCML(package=eea.facetednavigation)
        z2.installProduct(app, 'eea.facetednavigation')

    def setUpPloneSite(self, portal):
        """ Setup Plone
        """
        if LinguaPlone:
            applyProfile(portal, 'Products.LinguaPlone:LinguaPlone')
        applyProfile(portal, 'eea.facetednavigation:default')

        # Default workflow
        wftool = portal['portal_workflow']
        wftool.setDefaultChain('simple_publication_workflow')

        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])

        # Add default Plone content
        try:
            applyProfile(portal, 'plone.app.contenttypes:plone-content')
            # portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        except KeyError:
            # BBB Plone 4
            setuphandlers.setupPortalContent(portal)

        # Create testing environment
        portal.invokeFactory("Folder", "sandbox", title="Sandbox")


    def tearDownZope(self, app):
        """ Uninstall Zope
        """
        z2.uninstallProduct(app, 'eea.facetednavigation')

EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(EEAFIXTURE,),
                                       name='EEAFacetedNavigation:Functional')
