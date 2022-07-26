""" Adapters
"""
from eea.facetednavigation.interfaces import IWidgetFilterBrains
from zope.interface import implementer


@implementer(IWidgetFilterBrains)
class WidgetFilterBrains(object):
    """Filter brains after query"""

    def __init__(self, context):
        self.widget = context

    def __call__(self, brains, form):
        """Filter brains"""
        wid = self.widget.data.getId()
        index = self.widget.data.get("index", "")

        if self.widget.hidden:
            letter = self.widget.default
        else:
            letter = form.get(wid, "")

        if isinstance(letter, bytes):
            letter = letter.decode("utf-8", "replace")

        for brain in brains:
            if not (index and letter):
                yield brain
                continue

            if letter.lower() in ["all", "all"]:
                yield brain
                continue

            xval = getattr(brain, index, None)
            if xval is None:
                continue

            if not isinstance(xval, (bytes, str)):
                continue

            if isinstance(xval, bytes):
                xval = xval.decode("utf-8", "replace")

            if not xval.lower().startswith(letter.lower()):
                continue
            yield brain
