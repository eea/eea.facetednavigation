""" Alphabet widget
"""
import logging
from zope.interface import implements
from Products.Archetypes.public import Schema
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import BooleanWidget
from eea.facetednavigation.widgets.field import StringField

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from alphabets import unicode_character_map
from eea.facetednavigation.widgets.widget import CountableWidget

from interfaces import IAlphabeticWidget

logger = logging.getLogger('eea.facetednavigation.widgets.alphabetic')

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.AlphabeticCatalogIndexes',
        widget=SelectionWidget(
            format='select',
            label='Catalog index',
            label_msgid='faceted_criteria_index',
            description='Catalog index to use for search',
            description_msgid='help_faceted_criteria_index',
            i18n_domain="eea.facetednavigation"
        )
    ),
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label='Count results',
            label_msgid='faceted_criteria_count',
            description='Display number of results per letter',
            description_msgid='help_faceted_criteria_alphabetic_count',
            i18n_domain="eea.facetednavigation"
        )
    ),
    BooleanField('hidezerocount',
        schemata="countable",
        widget=BooleanWidget(
            label='Hide items with zero results',
            label_msgid='faceted_criteria_emptycounthide',
            description='This option works only if "count results" is enabled',
            description_msgid='help_faceted_criteria_criteria_emptycounthide',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=3,
            maxlength=1,
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default letter to be selected',
            description_msgid='help_faceted_criteria_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(CountableWidget):
    """ Widget
    """
    implements(IAlphabeticWidget)

    # Widget properties
    widget_type = 'alphabetic'
    widget_label = 'Alphabetic'
    view_js = '++resource++eea.facetednavigation.widgets.alphabets.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.alphabets.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.alphabets.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.alphabets.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = CountableWidget.edit_schema + EditSchema

    # Widget custom API
    def getAlphabet(self, lang):
        """ Get language alphabet
        """
        #TODO: also to implement 0-9 and Other on the alphabet listing
        try:
            lang = lang.split('-')[0].lower()
        except Exception, err:
            logger.exception(err)
            lang = 'en'
        return unicode_character_map.get(lang,
                    unicode_character_map.get('en'))

    def count(self, brains):
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

        for brain in brains:
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
        res['all'] = len(brains)
        return res
