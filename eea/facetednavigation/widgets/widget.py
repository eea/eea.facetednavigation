""" Abstract widgets
"""
import re
import logging
import operator
from zope import interface
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.i18nmessageid.message import Message
from zope.schema.interfaces import IVocabularyFactory
from zope.component import queryUtility
from BTrees.IIBTree import weightedIntersection, IISet
from zExceptions import NotFound

from plone.i18n.normalizer import urlnormalizer as normalizer
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safeToInt
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import SelectionWidget

from eea.facetednavigation.interfaces import IFacetedCatalog

from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.dexterity_support import normalize as atdx_normalize
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
            label=_(u"Friendly name"),
            description=_(u"Title for widget to display in view page"),
        )
    ),
    StringField('position',
        schemata="layout",
        vocabulary_factory="eea.faceted.vocabularies.WidgetPositions",
        widget=SelectionWidget(
            format='select',
            label=_(u'Position'),
            description=_(u"Widget position in page"),
        )
    ),
    StringField('section',
        schemata="layout",
        vocabulary_factory="eea.faceted.vocabularies.WidgetSections",
        widget=SelectionWidget(
            format='select',
            label=_(u"Section"),
            description=_("Display widget in section"),
        )
    ),
    BooleanField('hidden',
        schemata="layout",
        widget=BooleanWidget(
            label=_(u'Hidden'),
            description=_(u"Hide widget"),
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
        if value is not None:
            return value

        field = self.widget.edit_schema.get(self.key)
        return getattr(field, 'default', None)
#
# Widget wrapper for Archetypes Widgets
#
class ATWidget(BrowserView):
    """ Archetypes Widget
    """
    view_schema = Schema()
    edit_schema = CommonEditSchema.copy()

    def get_macro(self, field, schema='view'):
        """ Get edit macro from archetypes schema by given field name
        """
        field = self.get_field(field, schema)
        try:
            return field.widget('edit', self.context)
        except NotFound:
            # This hack makes this work for dexterity items - they do not
            # implement dict access (getitem), therefore we get a NotFound
            # when trying to get the 'at_widget_%s' customization element
            # - see Products/Archetypes/generator/widget.py
            # Trick Archetypes into avoid trying to get the 'at_widget_%s'
            # macro:
            field.widget.macro = field.widget.macro + '|dummy'
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
    def css_class(self):
        """ Widget specific css class
        """
        css_type = self.widget_type
        css_title = normalizer.normalize(self.data.title)
        return 'faceted-{0}-widget section-{1}'.format(css_type, css_title)

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
        index = self.data.get('index', None)
        if index == 'Language':
            language_widget = queryMultiAdapter((self, self.context),
                                                ILanguageWidgetAdapter)
            if language_widget:
                return language_widget.default
        # Take value from request parameter, for example ?SearchableText=test.
        from_request = self.request.form.pop(index, None)
        if from_request is not None:
            return from_request
        return self.data.get('default', None)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        return {}

    def translate(self, message):
        """ Use zope.i18n to translate message
        """
        if not message:
            return ''
        elif isinstance(message, Message):
            # message is an i18n message
            return translate(message, context=self.request)
        else:
            # message is a simple msgid
            for domain in ['eea', 'plone']:
                if isinstance(message, str):
                    try:
                        message = message.decode('utf-8')
                    except Exception, err:
                        logger.exception(err)
                        continue

                value = translate(message, domain=domain, context=self.request)
                if value != message:
                    return value
            return message

    def cleanup(self, string):
        """ Quote string
        """
        safe = re.compile(r'[^_A-Za-z0-9\-]')
        return safe.sub('-', string)

    def word_break(self, text='', insert="<wbr />", nchars=15):
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
            if isinstance(val, (int, float)):
                val = unicode(str(val), 'utf-8')

            elif not isinstance(val, unicode):
                try:
                    val = unicode(val, 'utf-8')
                except Exception:
                    continue

            val = val.strip()
            if not val:
                continue

            res.append(val)

        return res

    def portal_vocabulary(self):
        """Look up selected vocabulary from portal_vocabulary or from ZTK
           zope-vocabulary factory.
        """
        vtool = getToolByName(self.context, 'portal_vocabularies', None)
        voc_id = self.data.get('vocabulary', None)
        if not voc_id:
            return []
        voc = getattr(vtool, voc_id, None)
        if not voc:
            voc = queryUtility(IVocabularyFactory, voc_id, None)
            if voc:
                values = []
                for term in voc(self.context):
                    value = term.value
                    if isinstance(value, str):
                        value = value.decode('utf-8')
                    values.append((value, (term.title or term.token or value)))
                return values
            return []

        terms = voc.getDisplayList(self.context)
        if hasattr(terms, 'items'):
            return terms.items()
        return terms

    def vocabulary(self, **kwargs):
        """ Return data vocabulary
        """
        reverse = safeToInt(self.data.get('sortreversed', 0))
        mapping = self.portal_vocabulary()
        catalog = self.data.get('catalog', None)

        if catalog:
            mapping = dict(mapping)
            values = []
            try:
                from collective.solr.interfaces import ISearch
                searchutility = queryUtility(ISearch, None)
                if searchutility is not None:
                    index = self.data.get('index', None)
                    kw = {'facet': 'on',
                      'facet.field': index,    # facet on index
                      'facet.limit': -1,       # show unlimited results
                      'rows':0}                # no results needed
                    result = searchutility.search('*:*', **kw)
                    try:
                        values = result.facet_counts[
                            'facet_fields'][index].keys()
                    except (AttributeError, KeyError):
                        pass
            except ImportError:
                pass
            if not values:
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


CountableWidgetSchema = Schema((
    BooleanField('count',
        schemata="countable",
        widget=BooleanWidget(
            label=_(u"Count results"),
            description=_(u"Display number of results near each option"),
        )
    ),
    BooleanField('sortcountable',
        schemata="countable",
        widget=BooleanWidget(
            label=_(u"Sort by countable"),
            description=_(u"Use the results counter for sorting"),
        )
    ),
    BooleanField('hidezerocount',
        schemata="countable",
        widget=BooleanWidget(
            label=_(u'Hide items with zero results'),
            description=_(u"This option works only if 'count results' "
                           "is enabled"),
            i18n_domain="eea"
        )
    ),
))

class CountableWidget(Widget):
    """ Defines useful methods for countable widgets
    """
    # Widget properties
    edit_schema = Widget.edit_schema.copy() + CountableWidgetSchema.copy()

    @property
    def countable(self):
        """ Count results?
        """
        return bool(safeToInt(self.data.get('count', 0)))

    @property
    def sortcountable(self):
        """ Sort results by countable value?
        """
        return bool(safeToInt(self.data.get('sortcountable', 0)))

    @property
    def hidezerocount(self):
        """ Hide items that return no result?
        """
        return bool(safeToInt(self.data.get('hidezerocount', 0)))

    faceted_field = True

    def count(self, brains, sequence=None):
        """ Intersect results
        """
        res = {}
        # by checking for facet_counts we assume this is a SolrResponse
        # from collective.solr
        if hasattr(brains, 'facet_counts'):
            facet_fields = brains.facet_counts.get('facet_fields')
            if facet_fields:
                index_id = self.data.get('index')
                facet_field = facet_fields.get(index_id, {})
                for value, num in facet_field.items():
                    normalized_value = atdx_normalize(value)
                    if isinstance(value, unicode):
                        res[value] = num
                    elif isinstance(normalized_value, unicode):
                        res[normalized_value] = num
                    else:
                        unicode_value = value.decode('utf-8')
                        res[unicode_value] = num
            else:
                # no facet counts were returned. we exit anyway because
                # zcatalog methods throw an error on solr responses
                return res
            res[""] = res['all'] = len(brains)
            return res
        else:
            # this is handled by the zcatalog. see below
            pass

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
            normalized_value = atdx_normalize(value)
            rset = ctool.apply_index(self.context, index, normalized_value)[0]
            rset = IISet(rset)
            rset = weightedIntersection(brains, rset)[1]
            if isinstance(value, unicode):
                res[value] = len(rset)
            elif isinstance(normalized_value, unicode):
                res[normalized_value] = len(rset)
            else:
                unicode_value = value.decode('utf-8')
                res[unicode_value] = len(rset)
        return res
