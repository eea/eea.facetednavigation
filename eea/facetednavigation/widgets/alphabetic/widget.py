""" Alphabet widget
"""
import logging
from zope.interface import implementer

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation.widgets.alphabetic.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.alphabetic.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.alphabetic.alphabets import (
    unicode_character_map,
)
from eea.facetednavigation.widgets.alphabetic.interfaces import (
    IAlphabeticWidget,
)
logger = logging.getLogger('eea.facetednavigation.widgets.alphabetic')


@implementer(IAlphabeticWidget)
class Widget(CountableWidget):
    """ Widget
    """
    widget_type = 'alphabetic'
    widget_label = _('Alphabetic')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')

    # Widget custom API
    def getAlphabet(self, lang):
        """ Get language alphabet
        """
        try:
            lang = lang.split('-')[0].lower()
        except Exception, err:
            logger.exception(err)
            lang = 'en'
        return unicode_character_map.get(lang,
                    unicode_character_map.get('en'))

    def count(self, brains, sequence=None):
        """ Intersect results
        """
        res = {}
        lang = self.request.get('LANGUAGE', 'en')
        sequence = [item[0] for item in self.getAlphabet(lang)]
        if not sequence:
            return res

        index_id = self.data.get('index')
        if not index_id:
            return res

        index = 0
        for index, brain in enumerate(brains):
            xval = getattr(brain, index_id, None)
            if not xval:
                continue
            if not isinstance(xval, (str, unicode)):
                continue
            if isinstance(xval, str):
                xval = xval.decode('utf-8', 'replace')
            letter = xval[0].upper()
            count = res.get(letter, 0)
            res[letter] = count + 1
        res['all'] = index + 1
        return res
