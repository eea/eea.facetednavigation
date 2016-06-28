""" Main product initializer
"""
from Products.CMFPlone import interfaces as Plone
from zope.interface import implementer
from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')

@implementer(Plone.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            u'eea.facetednavigation:universal',
        ]


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
