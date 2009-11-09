""" Text widget
"""
import logging
from DateTime import DateTime
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DateTimeField
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from eea.facetednavigation.widgets.field import StringField

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
logger = logging.getLogger('eea.facetednavigation.widgets.daterange')

ViewSchema = Schema((
    DateTimeField('start',
        widget=CalendarWidget(
            label="Start Date",
            show_hm=False,
            label_msgid="label_date_range_criteria_start",
            i18n_domain="plone"),
    ),
    DateTimeField('end',
        widget=CalendarWidget(
            label="End Date",
            show_hm=False,
            label_msgid="label_date_range_criteria_end",
            i18n_domain="plone"),
    ),
))

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.DateRangeCatalogIndexes',
        widget=SelectionWidget(
            format='select',
            label='Catalog index',
            label_msgid='faceted_criteria_index',
            description='Catalog index to use for search',
            description_msgid='help_faceted_criteria_index',
            i18n_domain="eea.facetednavigation"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default daterange (e.g. "2009/12/01=>2009/12/31")',
            description_msgid='help_faceted_criteria_date_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class ViewAccessor(object):
    """ Return default start/end date
    """
    def __init__(self, data, key):
        self.data = data
        self.key = key

    def __call__(self):
        default = self.data.get('default', '')
        if not default:
            return None

        default = default.split('=>')
        if len(default) != 2:
            return None

        if self.key == 'start':
            start = default[0]
            try:
                start = DateTime(start.strip())
            except Exception, err:
                logger.exception('%s => Start date: %s', err, start)
                return None
            else:
                return start
        elif self.key == 'end':
            end = default[1]
            try:
                end = DateTime(end.strip())
            except Exception, err:
                logger.exception('%s => End date: %s', err, end)
                return None
            else:
                return end
        return None

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'daterange'
    widget_label = 'Date range'
    view_js = '++resource++eea.facetednavigation.widgets.daterange.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.daterange.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.daterange.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.daterange.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    view_schema = ViewSchema
    edit_schema = AbstractWidget.edit_schema + EditSchema

    def __init__(self, context, request, data=None):
        AbstractWidget.__init__(self, context, request, data)

    @property
    def default(self):
        """ Return default
        """
        return (self.view_accessor('start'), self.view_accessor('end'))

    def view_accessor(self, key):
        """ Accessor used in view mode
        """
        return ViewAccessor(self.data, key)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
            start, end = value
            start = start()
            end = end()
        else:
            value = form.get(self.data.getId(), ())
            if not value or len(value)!=2:
                return query
            start, end = value

        try:
            start = DateTime(start)
            end = DateTime(end)
        except Exception, err:
            logger.exception(err)
            return query

        query[index] = {
            'query': (start, end),
            'range': 'min:max'
        }
        return query
