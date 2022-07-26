""" Base test cases
"""
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.zope import installProduct
from plone.testing.zope import uninstallProduct
from Products.CMFPlone import setuphandlers


class EEAFixture(PloneSandboxLayer):
    """EEA Testing Policy"""

    def setUpZope(self, app, configurationContext):
        """Setup Zope"""
        import eea.facetednavigation

        self.loadZCML(package=eea.facetednavigation)
        installProduct(app, "eea.facetednavigation")

    def setUpPloneSite(self, portal):
        """Setup Plone"""
        applyProfile(portal, "eea.facetednavigation:default")

        # Default workflow
        wftool = portal["portal_workflow"]
        wftool.setDefaultChain("simple_publication_workflow")

        # Login as manager
        setRoles(portal, TEST_USER_ID, ["Manager"])

        # Add default Plone content
        try:
            applyProfile(portal, "plone.app.contenttypes:plone-content")
            # portal.portal_workflow.setDefaultChain(
            #     'simple_publication_workflow')
        except KeyError:
            # BBB Plone 4
            setuphandlers.setupPortalContent(portal)

        # Create testing environment
        portal.invokeFactory("Folder", "sandbox", title="Sandbox")

    def tearDownZope(self, app):
        """Uninstall Zope"""
        uninstallProduct(app, "eea.facetednavigation")


EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEAFIXTURE,), name="EEAFacetedNavigation:Functional"
)
