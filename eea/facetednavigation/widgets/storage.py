""" Criteria storage
"""
from zope import interface
from eea.facetednavigation.widgets.interfaces import ICriterion

class Criterion(object):
    """ Search criteria
    """
    interface.implements(ICriterion)

    widget = None
    title = ''
    index = ''
    vocabulary = ''
    position = 'right'
    catalog = None
    _hidden = False
    default = None
    section = 'default'

    def hidden(self=None):
        """ Hidden property
        """
        def fget(self):
            """ Getter
            """
            hidden = getattr(self, '_hidden', None)
            if not hidden:
                return False

            if hidden in ('0', 'False', 'false', 'none', 'None'):
                return False
            return True

        def fset(self, value):
            """ Setter
            """
            if value in ('0', 'False', 'false', 'none', 'None'):
                value = False
            self._hidden = value and True or False
        return property(fget, fset, doc='Hidden property')
    hidden = hidden()

    def __init__(self, **kwargs):
        taken_ids = set(kwargs.pop('_taken_ids_', []))
        cid = kwargs.pop('_cid_', None)
        if not cid:
            free_ids = set('c%d' % uid for uid in range(len(taken_ids)+1))
            cid = free_ids.difference(taken_ids)
            cid = cid.pop()
        elif cid in taken_ids:
            raise KeyError('Id is already in use')
        self.__name__ = cid
        self.update(**kwargs)

    def update(self, **kwargs):
        """ Update criterion properties
        """
        for key, value in kwargs.items():
            if isinstance(value, str):
                value = value.decode('utf-8', 'replace')

            if value == u'0':
                value = u""

            setattr(self, key, value)

    def getId(self):
        """ Get criterion id
        """
        return self.__name__

    def get(self, key, default=None):
        """ Get attribute by given key
        """
        return getattr(self, key, default)
