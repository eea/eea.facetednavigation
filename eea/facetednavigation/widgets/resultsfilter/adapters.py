""" Adapters
"""
from zope.interface import implementer
from eea.facetednavigation.interfaces import IWidgetFilterBrains


@implementer(IWidgetFilterBrains)
class WidgetFilterBrains(object):
    """ Filter brains after query
    """
    def __init__(self, context):
        self.widget = context

    def __call__(self, brains, form):
        """ Filter brains
        """
        for brain in brains:
            if self.widget.talexpr(brain):
                yield brain
