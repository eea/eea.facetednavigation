from p4a.subtyper.interfaces import ISubtyper
from zope.component import getUtility
from Products.statusmessages.interfaces import IStatusMessage

class FacetedSynchronizeTranslation(object):
    """ Faceted synchronize translations
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg=''):
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

        subtyper = getUtility(ISubtyper)
        subtype = subtyper.existing_type(canonical)
        subtype = getattr(subtype, 'name', None)
        if not subtype:
            self._redirect('Nothing to do')

        for lang in canonical.getTranslations().keys():
            translation = canonical.getTranslation(lang)
            if not translation:
                continue

            tr_subtype = subtyper.existing_type(translation)
            tr_subtype = getattr(tr_subtype, 'name', None)
            if tr_subtype != subtype:
                subtyper.change_type(translation, subtype)
        self._redirect('Faceted settings updated across translations')
