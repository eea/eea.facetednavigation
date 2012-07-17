""" Alphabet widget
"""
import logging
from zope.interface import implements
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.Archetypes.public import Schema
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget

from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation.widgets.alphabetic.alphabets import (
    unicode_character_map,
)
from eea.facetednavigation.widgets.alphabetic.interfaces import (
    IAlphabeticWidget,
)
from eea.facetednavigation import EEAMessageFactory as _

logger = logging.getLogger('eea.facetednavigation.widgets.alphabetic')

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.AlphabeticCatalogIndexes',
        widget=SelectionWidget(
            format='select',
            label=_(u"Catalog index"),
            description=_(u"Catalog index to use for search"),
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label=_(u"Count results"),
            description=_(u'Display number of results per letter'),
        )
    ),
    BooleanField('hidezerocount',
        schemata="countable",
        widget=BooleanWidget(
            label=_(u"Hide items with zero results"),
            description=_(u"This option works only if 'count results' "
                           "is enabled"),
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=3,
            maxlength=1,
            label=_(u"Default value"),
            description=_(u"Default letter to be selected"),
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    implements(IAlphabeticWidget)

    # Widget properties
    widget_type = 'alphabetic'
    widget_label = _('Alphabetic')
    view_js = '++resource++eea.facetednavigation.widgets.alphabets.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.alphabets.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.alphabets.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.alphabets.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema.copy() + EditSchema

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
            if type(xval) not in (str, unicode):
                continue
            if isinstance(xval, str):
                xval = xval.decode('utf-8', 'replace')
            letter = xval[0].upper()
            count = res.get(letter, 0)
            res[letter] = count + 1
        res['all'] = index
        return res
