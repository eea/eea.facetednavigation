""" Support for dexterity content-types
"""
from Products.CMFPlone.utils import safe_unicode


def normalize(value):
    """Normalize"""
    return safe_unicode(value)
