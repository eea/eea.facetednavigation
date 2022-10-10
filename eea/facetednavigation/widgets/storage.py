""" Criteria storage
"""
from eea.facetednavigation.widgets.interfaces import ICriterion
from Products.CMFPlone.utils import safe_unicode
from zope import interface


@interface.implementer(ICriterion)
class Criterion(object):
    """Search criteria"""

    widget = None
    title = ""
    index = ""
    vocabulary = ""
    position = "right"
    catalog = None
    _hidden = False
    custom_css = ""
    default = None
    section = "default"

    def __init__(self, **kwargs):
        taken_ids = set(kwargs.pop("_taken_ids_", []))
        cid = kwargs.pop("_cid_", None)
        if not cid:
            free_ids = set("c%d" % uid for uid in list(range(len(taken_ids) + 1)))
            cid = free_ids.difference(taken_ids)
            cid = sorted(cid).pop()
        elif cid in taken_ids:
            raise KeyError("Id is already in use")
        cid = safe_unicode(cid)
        self.__name__ = cid
        self.update(**kwargs)

    @property
    def hidden(self):
        """Hidden getter"""
        hidden = getattr(self, "_hidden", None)
        if not hidden:
            return False

        if hidden in ("0", "False", "false", "none", "None"):
            return False
        return True

    @hidden.setter
    def hidden(self, value):
        """Hidden setter"""
        if value in ("0", "False", "false", "none", "None"):
            value = False
        self._hidden = True if value else False

    def update(self, **kwargs):
        """Update criterion properties"""
        for key, value in kwargs.items():
            setattr(self, safe_unicode(key), safe_unicode(value))

    def getId(self):
        """Get criterion id"""
        return self.__name__

    def get(self, key, default=None):
        """Get attribute by given key"""
        return getattr(self, key, default)
