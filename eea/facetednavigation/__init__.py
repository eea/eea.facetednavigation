""" Main product initializer
"""
from zope.i18nmessageid.message import MessageFactory


_ = MessageFactory("eea")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
