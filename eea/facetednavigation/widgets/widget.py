""" Abstract widgets
"""
import re
import logging
import operator
from zope import interface
from zope.component import queryMultiAdapter
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import queryUtility
from BTrees.IIBTree import weightedIntersection, IISet

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import SelectionWidget
from eea.facetednavigation.widgets.field import StringField

from eea.facetednavigation.interfaces import IFacetedCatalog

from eea.facetednavigation.interfaces import ILanguageWidgetAdapter
from eea.facetednavigation.widgets.interfaces import IWidget

def compare(a, b):
    """ Compare lower values
    """
    return cmp(a.lower(), b.lower())

logger = logging.getLogger('eea.facetednavigation.widgets.widget')

CommonEditSchema = Schema((
    StringField('title',
        schemata="default",
        required=True,
        widget=StringWidget(
            size=25,
            label='Friendly name',
            label_msgid='faceted_criteria_title',
            description='Title for widget to display in view page',
            description_msgid='help_faceted_criteria_title',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('position',
        schemata="layout",
        vocabulary_factory="eea.faceted.vocabularies.WidgetPositions",
        widget=SelectionWidget(
            format='select',
            label='Position',
            label_msgid='faceted_criteria_position',
            description='Widget position in page',
            description_msgid='help_faceted_criteria_position',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('section',
        schemata="layout",
        vocabulary_factory="eea.faceted.vocabularies.WidgetSections",
        widget=SelectionWidget(
            format='select',
            label='Section',
            label_msgid='faceted_criteria_section',
            description='Display widget in section',
            description_msgid='help_faceted_criteria_section',
            i18n_domain="eea.facetednavigation"
        )
    ),
    BooleanField('hidden',
        schemata="layout",
        widget=BooleanWidget(
            label='Hidden',
            label_msgid='faceted_criteria_hidden',
            description='Hide widget',
            description_msgid='help_faceted_criteria_hidden',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class SimpleATAccessor(object):
    """ Simple AT Accessor
    """
    def __init__(self, widget, key):
        self.widget = widget
        self.data = widget.data
        self.key = key

    def __call__(self):
        value = self.data.get(self.key, None)
        if value:
            return value

        schema = self.widget.edit_schema
        field = self.widget.edit_schema.get(self.key)
        return getattr(field, 'default', None)
#
# Widget wrapper for Archetypes Widgets
#
class ATWidget(BrowserView):
    """ Archetypes Widget
    """
    view_schema = Schema()
    edit_schema = CommonEditSchema

    def get_macro(self, field, schema='view'):
        """ Get edit macro from archetypes schema by given field name
        """
        field = self.get_field(field, schema)
        return field.widget('edit', self.context)

    def get_field(self, field, schema='view'):
        """ Get field from archetypes schema by given field name
        """
        if schema == 'view':
            return self.view_schema[field]
        return self.edit_schema[field]

    def accessor(self, key):
        """ Returns a value accessor
        """
        return SimpleATAccessor(self, key)
#
# Faceted Widget
#
class Widget(ATWidget):
    """ All faceted widgets should inherit from this class
    """
    interface.implements(IWidget)

    # Widget properties
    widget_type = 'abstract'
    widget_label = 'Abstract'
    view_css = ()
    edit_css = ()
    view_js = ()
    edit_js = ()
    index = None

    def __init__(self, context, request, data=None):
        self.context = context
        self.request = request
        self.request.debug = False
        self.data = data

    @property
    def template(self):
        """ Widget template
        """
        return self.index()

    @property
    def hidden(self):
        """ Widget hidden?
        """
        return self.data.hidden

    @property
    def default(self):
        """ Get default values
        """
        # Language widget has custom behaviour so be sure you keep
        # this in your widget
        if self.data.get('index', None) == 'Language':
            language_widget = queryMultiAdapter((self, self.context),
                                                ILanguageWidgetAdapter)
            if language_widget:
                return language_widget.default
        return self.data.get('default', None)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        return {}

    def translate(self, msgid):
        """ Use PloneMessageFactory to translate msgid
        """
        if not msgid:
            return ''

        tool = getToolByName(self.context, 'translation_service')
        for domain in ['eea.facetednavigation', 'eea.faceted',
                       'eea.translations', 'plone']:
            try:
                value = tool.utranslate(domain, msgid, {}, context=self.context,
                            target_language=self.request.get('LANGUAGE', 'en'),
                            default=msgid)
            except Exception, err:
                logger.exception(err)
                continue

            try:
                if not isinstance(value, unicode):
                    value = value.decode('utf-8')
                if not isinstance(msgid, unicode):
                    msgid = msgid.decode('utf-8')
            except Exception, err:
                logger.exception(err)
                continue

            if value != msgid:
                return value
        return msgid

    def cleanup(self, string):
        """ Quote string
        """
        safe = re.compile(r'[^_A-Za-z0-9\-]')
        return safe.sub('-', string)

    def word_break(self, text='', insert="<wbr />", nchars=5):
        """ Insert a string (insert) every space or if a word length is bigger
        than given chars, every ${chars} characters.

        Example:
        >>> text = 'this is a bigwordwith_and-and.jpg'
        >>> print word_break(text, nchars=10)
        this is a bigwordwit<wbr />h_and-and.<wbr />jpg
        """
        list_text = text.split(' ')
        res = []
        for word in list_text:
            word = [word[i:i + nchars] for i in xrange(0, len(word), nchars)]
            word = insert.join(word)
            res.append(word)
        return ' '.join(res)

    def catalog_vocabulary(self):
        """ Get vocabulary from catalog
        """
        catalog = self.data.get('catalog', 'portal_catalog')
        ctool = getToolByName(self.context, catalog)
        if not ctool:
            return []
        index = self.data.get('index', None)
        if not index:
            return []
        index = ctool.Indexes.get(index, None)
        if not index:
            return []

        res = []
        for val in index.uniqueValues():
            if not isinstance(val, unicode):
                try:
                    val = unicode(val, 'utf-8')
                except Exception, err:
                    continue

            val = val.strip()
            if not val:
                continue
            res.append(val)
        return res

    def portal_vocabulary(self):
        """ Return data vocabulary
        """
        vtool = getToolByName(self.context, 'portal_vocabularies', None)
        voc_id = self.data.get('vocabulary', None)
        if not voc_id:
            return []
        voc = getattr(vtool, voc_id, None)
        if not voc:
            voc = queryUtility(IVocabularyFactory, voc_id, None)
            if voc:
                return [(term.value, (term.title or term.token or term.value))
                        for term in voc(self.context)]
            return []

        terms = voc.getDisplayList(self.context)
        if hasattr(terms, 'items'):
            return terms.items()
        return terms

    def vocabulary(self):
        """ Return data vocabulary
        """
        reverse = self.data.get('sortreversed', False)
        try:
            reverse = int(reverse)
        except (ValueError, TypeError):
            reverse = 0

        mapping = self.portal_vocabulary()
        catalog = self.data.get('catalog', None)

        if catalog:
            mapping = dict(mapping)
            values = self.catalog_vocabulary()
            res = [(val, mapping.get(val, val)) for val in values]
            res.sort(key=operator.itemgetter(1), cmp=compare)
        else:
            res = mapping

        if reverse:
            res.reverse()
        return res

    def __call__(self, **kwargs):
        """
        """
        return self.template

class CountableWidget(Widget):
    """ Define usefull methods for countable widgets
    """
    @property
    def countable(self):
        """ Count results ?
        """
        count = self.data.get('count', False)
        if not count:
            return False

        try:
            count = int(count)
        except (TypeError, ValueError):
            return False
        return not not count

    @property
    def hidezerocount(self):
        """ Hide items that return no result ?
        """
        hide = self.data.get('hidezerocount', False)
        if not hide:
            return False

        try:
            hide = int(hide)
        except (TypeError, ValueError):
            return False
        return not not hide

    def count(self, brains, sequence=None):
        """ Intersect results
        """
        res = {}
        if not sequence:
            sequence = [key for key, value in self.vocabulary()]

        if not sequence:
            return res

        index_id = self.data.get('index')
        if not index_id:
            return res

        ctool = getToolByName(self.context, 'portal_catalog')
        index = ctool._catalog.getIndex(index_id)
        ctool = queryUtility(IFacetedCatalog)
        if not ctool:
            return res

        brains = IISet(brain.getRID() for brain in brains)
        res[""] = res['all'] = len(brains)
        for value in sequence:
            if not value:
                res[value] = len(brains)
                continue
            if isinstance(value, unicode):
                try:
                    value = value.encode('utf-8')
                except Exception, err:
                    continue
            rset, u = ctool.apply_index(self.context, index, value)
            rset = IISet(rset)
            u, rset = weightedIntersection(brains, rset)
            if isinstance(value, str):
                try:
                    value = value.decode('utf-8')
                except Exception, err:
                    continue
            res[value] = len(rset)
        return res
