""" Abstract widgets
"""
import re
import logging
import operator
from zope import interface
from z3c.form import form, group
from z3c.form.interfaces import IGroup
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.i18nmessageid.message import Message
from zope.schema.interfaces import IVocabularyFactory
from zope.component import queryUtility
from BTrees.IIBTree import weightedIntersection, IISet

from plone.i18n.normalizer import urlnormalizer as normalizer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safeToInt
from Products.ZCatalog.Lazy import LazyMap

from eea.facetednavigation.plonex import ISolrSearch
from eea.facetednavigation.interfaces import IFacetedCatalog
from eea.facetednavigation.dexterity_support import normalize as atdx_normalize
from eea.facetednavigation.interfaces import ILanguageWidgetAdapter
from eea.facetednavigation.widgets.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.interfaces import CountableSchemata
logger = logging.getLogger('eea.facetednavigation')

def compare(a, b):
    """ Compare lower values
    """
    return cmp(a.lower(), b.lower())

#
# Faceted Widget
#
@interface.implementer(IWidget)
class Widget(group.GroupForm, form.Form):
    """ All faceted widgets should inherit from this class
    """
    # z3c.form
    groups = (DefaultSchemata, LayoutSchemata)

    # Faceted Widget properties
    widget_type = 'abstract'
    widget_label = 'Abstract'

    def __init__(self, context, request, data=None):
        self.context = context
        self.request = request
        self.request.debug = False
        self.data = data

    @property
    def prefix(self):
        """ Form prefix
        """
        cid = self.data.getId()
        if isinstance(cid, unicode):
            cid = cid.encode('utf-8')
        return cid

    def getContent(self):
        """ Content
        """
        return self.data

    def update(self):
        """ Update
        """
        self.updateWidgets(prefix=self.prefix)
        groups = []
        for groupClass in self.groups:
            if IGroup.providedBy(groupClass):
                group = groupClass
            else:
                group = groupClass(self.data, self.request, self)
            group.updateWidgets(prefix=self.prefix)
            groups.append(group)
        self.groups = tuple(groups)

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

            # get values from SOLR if collective.solr is present
            searchutility = queryUtility(ISolrSearch, None)
            if searchutility is not None:
                index = self.data.get('index', None)
                kw = {'facet': 'on',
                  'facet.field': index,    # facet on index
                  'facet.limit': -1,       # show unlimited results
                  'rows':0}                # no results needed
                result = searchutility.search('*:*', **kw)
                try:
                    values = result.facet_counts['facet_fields'][index].keys()
                except (AttributeError, KeyError):
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

class CountableWidget(Widget):
    """ Defines useful methods for countable widgets
    """
    groups = Widget.groups + (CountableSchemata,)

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

        if isinstance(brains, LazyMap):
            values = brains._seq
            # 75384 seq might be a pair of tuples instead of ints
            # if you upgrade to ZCatalog 3
            if isinstance(values[0], tuple):
                values = [v[1] for v in values]
            brains = IISet(values)
        else:
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
