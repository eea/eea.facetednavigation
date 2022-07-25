""" Sorting widget
"""
from zope.component import getUtility
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.registry.interfaces import IRegistry
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.sorting.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.sorting.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _
from Products.CMFCore.utils import getToolByName
try:
    from Products.ATContentTypes.criteria import _criterionRegistry
    HAS_ATCT = True
except ImportError:
    HAS_ATCT = False


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'sorting'
    widget_label = _('Sorting')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Return default sorting values
        """
        default = self.data.get('default', '')
        if not default:
            return ()
        reverse = False
        if '(reverse)' in default:
            default = default.replace('(reverse)', '', 1)
            reverse = True
        default = default.strip()
        return (default, reverse)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}

        if self.hidden:
            default = self.default
            sort_on = default[0] if default else None
            reverse = default[1] if len(default) > 1 else False
        else:
            sort_on = form.get(self.data.getId(), '')
            reverse = form.get('reversed', False)

        if sort_on:
            query['sort_on'] = sort_on

        if reverse:
            query['sort_order'] = 'descending'
        else:
            query['sort_order'] = 'ascending'

        return query

    def criteriaByIndexId(self, indexId):
        """ Get criteria by index id

        XXX: this method is probaly orphaned code
        """
        catalog_tool = getToolByName(self.context, 'portal_catalog')
        try:
            indexObj = catalog_tool.Indexes[indexId]
        except KeyError:
            return []
        # allow DateRecurringIndex that is unknown to atct.
        # events in plone.app.contenttypes use it for start and end
        if indexObj.meta_type == "DateRecurringIndex":
            return ('ATFriendlyDateCriteria',
                    'ATDateRangeCriterion',
                    'ATSortCriterion')
        results = _criterionRegistry.criteriaByIndex(indexObj.meta_type)
        return results

    def validateAddCriterion(self, indexId, criteriaType):
        """Is criteriaType acceptable criteria for indexId

        XXX: this method is probaly orphaned code
        """
        if HAS_ATCT:
            return criteriaType in self.criteriaByIndexId(indexId)
        return True

    def listSortFields(self):
        """Return a list of available fields for sorting."""

        registry = getUtility(IRegistry)
        config = IQuerystringRegistryReader(registry)()
        indexes = config.get('sortable_indexes', {})

        for name, index in indexes.items():
            title = index.get('title', name)
            description = index.get('description', title)
            yield (name, title, description)

    def vocabulary(self, **kwargs):
        """ Return data vocabulary
        """
        vocab = self.portal_vocabulary()
        sort_fields = [x for x in self.listSortFields()]

        if not vocab:
            return sort_fields

        vocab_fields = [(x[0].replace('term.', '', 1), x[1], '') for x in vocab]
        sort_field_ids = [x[0] for x in sort_fields]

        return [f for f in vocab_fields if f[0] in sort_field_ids]
