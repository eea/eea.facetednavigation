""" Text widget
"""
import logging

from DateTime import DateTime
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget

from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _


logger = logging.getLogger('eea.facetednavigation.widgets.daterange')

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.DateRangeCatalogIndexes',
        widget=SelectionWidget(
            format='select',
            label=_(u'faceted_criteria_index',
                default=u'Catalog index'),
            description=_(u'help_faceted_criteria_index',
                default=u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_('faceted_criteria_default',
                default='Default value'),
            description=_(u'help_faceted_criteria_daterange_default',
                default=u'Default daterange (e.g. "2009/12/01=>2009/12/31")'),
            i18n_domain="eea"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'daterange'
    widget_label = _('Date range')
    view_js = '++resource++eea.facetednavigation.widgets.daterange.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.daterange.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.daterange.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.daterange.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema

    @property
    def default(self):
        """ Return default
        """
        default = self.data.get('default', '')
        if not default:
            return ('', '')

        default = default.split('=>')
        if len(default) != 2:
            return ('', '')

        start, end = default
        try:
            start = DateTime(start.strip())
            start = start.strftime('%Y-%m-%d')
        except Exception, err:
            logger.exception('%s => Start date: %s', err, start)
            start = ''

        try:
            end = DateTime(end.strip())
            end = end.strftime('%Y-%m-%d')
        except Exception, err:
            logger.exception('%s => End date: %s', err, end)
            end = ''
        return (start, end)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            start, end = self.default
        else:
            value = form.get(self.data.getId(), ())
            if not value or len(value)!=2:
                return query
            start, end = value

        if not (start and end):
            return query

        try:
            start = DateTime(start)
            end = DateTime(end)
        except Exception, err:
            logger.exception(err)
            return query

        start = start - 1
        start = start.latestTime()
        end = end.latestTime()

        query[index] = {
            'query': (start, end),
            'range': 'min:max'
        }
        return query
