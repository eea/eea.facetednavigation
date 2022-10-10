""" Custom preview items
"""
from eea.facetednavigation.utils import truncate
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from zope.component.hooks import getSite

import logging


logger = logging.getLogger("eea.facetednavigation")


class PreviewItem(BrowserView):
    """Custom item tile"""

    def title(self):
        """Item title"""
        return self.context.Title()

    def description(self):
        """Item description"""
        return truncate(self.context.Description())

    def thumb(self):
        """Item thumb"""
        scale = queryMultiAdapter((self.context, self.request), name="images")
        if not scale:
            return ""
        return scale.tag("image", scale="mini")

    def url(self):
        """URL"""
        return self.context.absolute_url()


class PreviewBrain(PreviewItem):
    """Custom tile based on brain"""

    def __init__(self, context, request):
        super(PreviewBrain, self).__init__(context, request)
        self._brain = None

    @property
    def brain(self):
        """Brain"""
        return self._brain

    def description(self):
        """Description"""
        return truncate(self.brain.Description)

    def title(self):
        """Title"""
        return self.brain.Title

    def thumb(self):
        """Get Ad image"""
        site = getSite()
        image_scale = queryMultiAdapter((site, self.request), name="image_scale")
        if not image_scale:
            return ""
        try:
            return image_scale.tag(self.brain, "image", scale="mini")
        except AttributeError:
            return ""

    def url(self):
        """URL"""
        return getattr(self.brain, "getURL", lambda: "#")()

    def __call__(self, brain):
        self._brain = brain
        return super(PreviewBrain, self).__call__()
