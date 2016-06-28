""" Plone X compatibility over time
"""
from zope.interface import Interface
from Products.Five.browser import BrowserView
#
# plone.protect
#

try:
    from plone.protect import utils
    addTokenToUrl = utils.addTokenToUrl
except (ImportError, AttributeError):
    # BBB Plone 4
    def addTokenToUrl(url, *args, **kwargs):
        """ plone.protect
        """
        return url

try:
    from plone.protect import interfaces as protect
    IDisableCSRFProtection = protect.IDisableCSRFProtection
except (ImportError, AttributeError):
    # BBB Plone 4
    class IDisableCSRFProtection(Interface):
        """ Fallback
        """

#
# plone.app.contenttypes
#

try:
    from plone.app.contenttypes.browser import folder
    FolderView = folder.FolderView
except (ImportError, AttributeError):
    # BBB Plone 4
    class FolderView(BrowserView):
        """ Fallback Folder View
        """

#
# plone.app.querystring
#

try:
    from plone.app.querystring import queryparser
    parseFormquery = queryparser.parseFormquery
except (ImportError, AttributeError):
    def parseFormquery(*args, **kwargs):
        """ plone.app.querystring not installed
        """
        return {}

#
# collective.solr
#

try:
    from collective.solr import interfaces
    ISolrConnectionManager = interfaces.ISolrConnectionManager
    ISolrSearch = interfaces.ISearch
except (ImportError, AttributeError):
    class ISolrConnectionManager(Interface):
        """ collective.solr not installed
        """

    class ISolrSearch(Interface):
        """ collective.solr not installed
        """

#
# Older imports
#

try:
    from zope.browserpage import viewpagetemplatefile
    ViewPageTemplateFile = viewpagetemplatefile.ViewPageTemplateFile
except (ImportError, AttributeError):
    # BBB Plone < 4.3
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

try:
    from zope.pagetemplate import engine
    TrustedEngine = engine.TrustedEngine
    TrustedZopeContext = engine.TrustedZopeContext
except (ImportError, AttributeError):
    # BBB Plone < 4.3
    from zope.app.pagetemplate.engine import TrustedEngine, TrustedZopeContext

try:
    from zope.browsermenu import menu
    BrowserSubMenuItem = menu.BrowserSubMenuItem
except (ImportError, AttributeError):
    # BBB Plone < 4.3
    from zope.app.publisher.browser.menu import BrowserSubMenuItem

try:
    from zope.browsermenu import menu
    BrowserMenu = menu.BrowserMenu
except (ImportError, AttributeError):
    # BBB Plone < 4.3
    from zope.app.publisher.browser.menu import BrowserMenu
