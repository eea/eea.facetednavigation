""" Criteria storage
"""
from zope import interface
from eea.facetednavigation.widgets.interfaces import ICriterion

@interface.implementer(ICriterion)
class Criterion(object):
    """ Search criteria
    """
    widget = None
    title = u''
    index = u''
    vocabulary = u''
    position = u'right'
    catalog = None
    _hidden = False
    default = None
    section = u'default'

    def __init__(self, **kwargs):
        taken_ids = set(kwargs.pop(u'_taken_ids_', []))
        cid = kwargs.pop(u'_cid_', None)
        if not cid:
            free_ids = set(u'c%d' % uid for uid in range(len(taken_ids)+1))
            cid = free_ids.difference(taken_ids)
            cid = cid.pop()
        elif cid in taken_ids:
            raise KeyError(u'Id is already in use')
        if isinstance(cid, str):
            cid = cid.decode('utf-8')
        self.__name__ = cid
        self.update(**kwargs)

    @property
    def hidden(self):
        """ Hidden getter
        """
        hidden = getattr(self, u'_hidden', None)
        if not hidden:
            return False

        if hidden in (u'0', u'False', u'false', u'none', u'None'):
            return False
        return True

    @hidden.setter
    def hidden(self, value):
        """ Hidden setter
        """
        if value in (u'0', u'False', u'false', u'none', u'None'):
            value = False
        self._hidden = value and True or False

    def update(self, **kwargs):
        """ Update criterion properties
        """
        for key, value in kwargs.items():
            if isinstance(key, str):
                key = key.decode('utf-8')

            if isinstance(value, str):
                value = value.decode('utf-8', 'replace')

            setattr(self, key, value)

    def getId(self):
        """ Get criterion id
        """
        return self.__name__

    def get(self, key, default=None):
        """ Get attribute by given key
        """
        return getattr(self, key, default)
