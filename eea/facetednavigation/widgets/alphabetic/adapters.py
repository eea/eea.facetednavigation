""" Adapters
"""
from zope.interface import implements
from eea.facetednavigation.interfaces import IWidgetFilterBrains

class WidgetFilterBrains(object):
    """ Filter brains after query
    """
    implements(IWidgetFilterBrains)

    def __init__(self, context):
        self.widget = context

    def __call__(self, brains, form):
        """ Filter brains
        """
        wid = self.widget.data.getId()
        index = self.widget.data.get('index', '')

        if self.widget.hidden:
            letter = self.widget.default
        else:
            letter = form.get(wid, '')

        if isinstance(letter, str):
            letter = letter.decode('utf-8', 'replace')

        for brain in brains:
            if not (index and letter):
                yield brain
                continue

            if letter.lower() in [u'all', 'all']:
                yield brain
                continue

            xval = getattr(brain, index, None)
            if xval is None:
                continue

            if not isinstance(xval, (str, unicode)):
                continue

            if isinstance(xval, str):
                xval = xval.decode('utf-8', 'replace')

            if not xval.lower().startswith(letter.lower()):
                continue
            yield brain
