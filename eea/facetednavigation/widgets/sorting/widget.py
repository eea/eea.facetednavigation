""" Sorting widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.criteria import _criterionRegistry

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _


EditSchema = Schema((
    StringField('vocabulary',
        schemata="default",
        vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
        widget=SelectionWidget(
            label=_(u'Filter from vocabulary'),
            description=_(u'Vocabulary to use to filter sorting criteria. '
                        u'Leave empty for default sorting criteria.'),
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_(u'Default value'),
            description=_(u"Default sorting index "
                        u"(e.g. 'effective' or 'effective(reverse)')"),
            i18n_domain="eea"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'sorting'
    widget_label = _('Sorting')
    view_js = '++resource++eea.facetednavigation.widgets.sorting.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.sorting.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.sorting.view.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'Sort on'

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
            sort_on = len(default) > 0 and default[0] or None
            reverse = len(default) > 1 and default[1] or False
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
        """
        catalog_tool = getToolByName(self.context, 'portal_catalog')
        indexObj = catalog_tool.Indexes[indexId]
        results = _criterionRegistry.criteriaByIndex(indexObj.meta_type)
        return results

    def validateAddCriterion(self, indexId, criteriaType):
        """Is criteriaType acceptable criteria for indexId
        """
        return criteriaType in self.criteriaByIndexId(indexId)

    def listFields(self):
        """Return a list of fields from portal_catalog.
        """
        tool = getToolByName(self.context, 'portal_atct')
        return tool.getEnabledFields()

    def listSortFields(self):
        """Return a list of available fields for sorting."""
        fields = [ field
                    for field in self.listFields()
                    if self.validateAddCriterion(field[0], 'ATSortCriterion') ]
        return fields

    def vocabulary(self, **kwargs):
        """ Return data vocabulary
        """
        vocab = self.portal_vocabulary()
        sort_fields = self.listSortFields()
        if not vocab:
            return sort_fields

        vocab_fields = [field[0].replace('term.', '', 1) for field in vocab]
        return [f for f in sort_fields if f[0] in vocab_fields]
