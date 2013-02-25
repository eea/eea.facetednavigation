""" Faceted global settings
"""
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

__names__ = [
    BrowserSubMenuItem.__name__,
    BrowserMenu.__name__,
]
