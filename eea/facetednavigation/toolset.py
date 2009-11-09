try:
    from Products.CMFCore.fiveactionstool import FiveActionsTool
except ImportError:
    #BBB Plone 2.5
    from Products.CMFonFive.fiveactionstool import FiveActionsTool
