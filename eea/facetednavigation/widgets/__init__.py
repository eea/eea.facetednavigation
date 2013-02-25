""" Faceted widgets
"""
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

__names__ = [
    ViewPageTemplateFile.__name__,
    TrustedZopeContext.__name__,
    TrustedEngine,
]
