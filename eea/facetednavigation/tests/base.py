""" Base test cases
"""
from plone.testing import z2
from plone.app.testing import TEST_USER_ID
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from Products.CMFPlone import setuphandlers
from plone.app.testing import setRoles

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
        applyProfile(portal, 'eea.facetednavigation:default')

        # Default workflow
        wftool = portal['portal_workflow']
        wftool.setDefaultChain('simple_publication_workflow')

        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])

        # Add default Plone content
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


# import os
# from StringIO import StringIO
# from App.Common import package_home
# from cgi import FieldStorage
# from ZPublisher.HTTPRequest import FileUpload
# from Zope2.App import zcml
# from Products.Five import fiveconfigure
# from Products.PloneTestCase import PloneTestCase as ptc
# from Products.PloneTestCase.layer import onsetup
#
# ptc.installProduct('Five')
# ptc.installProduct('FiveSite')
# ptc.installProduct('ATVocabularyManager')
# ptc.installProduct('PloneLanguageTool')
# ptc.installProduct('LinguaPlone')
#
# product_globals = globals()
#
# @onsetup
# def setup_eea_facetednavigation():
#     """Set up the additional products required for the Report Content.
#
#     The @onsetup decorator causes the execution of this body to be deferred
#     until the setup of the Plone site testing layer.
#     """
#     fiveconfigure.debug_mode = True
#     from eea import facetednavigation
#     zcml.load_config('meta.zcml', facetednavigation)
#     zcml.load_config('overrides.zcml', facetednavigation)
#     zcml.load_config('configure.zcml', facetednavigation.subtypes)
#     zcml.load_config('configure.zcml', facetednavigation)
#     zcml.load_config('autocomplete.zcml', facetednavigation.tests)
#     fiveconfigure.debug_mode = False
#
# setup_eea_facetednavigation()
# ptc.setupPloneSite(
#     products=['ATVocabularyManager', 'LinguaPlone'],
#     extension_profiles=("eea.facetednavigation:default",)
# )
#
# class FacetedTestCase(ptc.PloneTestCase):
#     """Base class for integration tests for the 'FacetedNavigation' product.
#     """
#
# class FacetedFunctionalTestCase(ptc.FunctionalTestCase, FacetedTestCase):
#     """Base class for functional integration tests
#     for the 'FacetedNavigation' product.
#     """
#     def loadfile(self, rel_filename, ctype='text/xml'):
#         """ load a file
#         """
#         home = package_home(product_globals)
#         filename = os.path.sep.join([home, rel_filename])
#         data = open(filename, 'r').read()
#
#         fp = StringIO(data)
#         fp.seek(0)
#
#         header_filename = rel_filename.split('/')[-1]
#         env = {'REQUEST_METHOD':'PUT'}
#         headers = {'content-type' : ctype,
#                    'content-length': len(data),
#                    'content-disposition':'attachment; filename=%s' % (
#                        header_filename,
#                    )}
#
#         fs = FieldStorage(fp=fp, environ=env, headers=headers)
#         return FileUpload(fs)
