""" Sync translations
"""
from zope.component import getMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage

class FacetedSynchronizeTranslation(object):
    """ Faceted synchronize translations
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg=''):
        """ Set status message and redirect
        """
        to = self.request.get('redirect', self.context.absolute_url())
        if not to:
            return msg

        if msg:
            IStatusMessage(self.request).addStatusMessage(str(msg), type='info')
        self.request.response.redirect(to)

    def __call__(self, *args, **kwargs):
        """ Subtype all translations as faceted navigable
        """
        canonical = getattr(self.context, 'getCanonical', None)
        # LinguaPlone not present
        if not canonical:
            return
        canonical = canonical()

        subtyper = getMultiAdapter((canonical, self.request),
                                   name=u'faceted_subtyper')

        # Not a faceted navigable
        if not subtyper.can_disable:
            self._redirect('Nothing to do')

        for lang in canonical.getTranslations().keys():
            translation = canonical.getTranslation(lang)
            if not translation:
                continue

            subtyper = getMultiAdapter((translation, self.request),
                                       name=u'faceted_subtyper')
            subtyper.enable()

        self._redirect('Faceted settings updated across translations')
