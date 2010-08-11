""" Backward compatibility
"""

from Products.CMFCore.utils import getToolByName

try:
    import zope.annotation
except ImportError:
    #BBB Plone 2.5
    def setupVarious(context):
        """ Do some various setup.
        """
        site = context.getSite()
        setup_tool = getToolByName(site, 'portal_setup')

        # jQuery
        setup_tool.setImportContext('profile-eea.jquery:01-jquery')
        setup_tool.runAllImportSteps()

        # jQuery UI
        setup_tool.setImportContext('profile-eea.jquery:02-ui')
        setup_tool.runAllImportSteps()

        # Ajax FileUpload
        setup_tool.setImportContext('profile-eea.jquery:03-ajaxfileupload')
        setup_tool.runAllImportSteps()

        # jQuery BBQ
        setup_tool.setImportContext('profile-eea.jquery:04-bbq')
        setup_tool.runAllImportSteps()

        # jQuery Cookie
        setup_tool.setImportContext('profile-eea.jquery:05-cookie')
        setup_tool.runAllImportSteps()

        # JS Tree
        setup_tool.setImportContext('profile-eea.jquery:10-jstree')
        setup_tool.runAllImportSteps()

        # Select 2 uislider
        setup_tool.setImportContext('profile-eea.jquery:12-select2uislider')
        setup_tool.runAllImportSteps()

        # jQuery TagCloud
        setup_tool.setImportContext('profile-eea.jquery:14-tagcloud')
        setup_tool.runAllImportSteps()

        setup_tool.setImportContext('profile-eea.facetednavigation:default')
        return
else:
    # Plone 3+
    def setupVarious(context):
        """ Do some various setup.
        """
        return
