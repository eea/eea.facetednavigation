""" Text widget
"""
import logging
import re
from DateTime import DateTime
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import Schema
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget
from eea.facetednavigation.widgets.field import StringField

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

logger = logging.getLogger('eea.facetednavigation.widgets.daterange')

DateOptionsVocabulary = DisplayList((
    ('', 'All'),
    (0, 'Now'),
    (1, '1 Day'),
    (2, '2 Days'),
    (5, '5 Days'),
    (7, '1 Week'),
    (14, '2 Weeks'),
    (31, '1 Month'),
    (31*3, '3 Months'),
    (31*6, '6 Months'),
    (365, '1 Year'),
    (365*2, '2 Years'),
))

CompareOperationsVocabulary = DisplayList((
    ('', 'All'),
    ('more', 'More than'),
    ('less', 'Less than'),
    ('equal', 'On the day'),
))

RangeOperationsVocabulary = DisplayList((
    ('', 'All'),
    ('past', 'in the past'),
    ('future', 'in the future'),
))

ViewSchema = Schema((
    StringField('operation',
        vocabulary=CompareOperationsVocabulary,
        widget=SelectionWidget(
            label="More or less",
            label_msgid="label_date_criteria_operation",
            description="Select the date criteria operation.",
            description_msgid="help_date_criteria_operation",
            i18n_domain="atcontenttypes",
            format="select"),
    ),
    IntegerField('value',
        vocabulary=DateOptionsVocabulary,
        widget=SelectionWidget(
            label="Which day",
            label_msgid="label_date_criteria_value",
            description="Select the date criteria value.",
            description_msgid="help_date_criteria_value",
            i18n_domain="atcontenttypes"),
    ),
    StringField('daterange',
        vocabulary=RangeOperationsVocabulary,
        widget=SelectionWidget(
            label="In the past or future",
            label_msgid="label_date_criteria_range",
            description="Select the date criteria range. Ignore this if you selected 'Now' above.",
            description_msgid="help_date_criteria_range",
            i18n_domain="atcontenttypes",
            format="select"),
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
            description='Default daterange (e.g. "more than 3 days in the past" or "equal 1 day in the future")',
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
            return ''

        if self.key == 'operation':
            if 'less' in default:
                return 'less'
            if 'more' in default:
                return 'more'
            return 'equal'
        if self.key == 'daterange':
            if 'past' in default:
                return 'past'
            return 'future'
        if self.key == 'value':
            res = re.search(r'\d+', default)
            if not res:
                return 0
            return int(res.group(0))
        return ''

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'date'
    widget_label = 'Date'
    view_js = '++resource++eea.facetednavigation.widgets.date.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.date.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.date.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.date.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    view_schema = ViewSchema
    edit_schema = AbstractWidget.edit_schema + EditSchema

    def __init__(self, context, request, data=None):
        AbstractWidget.__init__(self, context, request, data)

    @property
    def default(self):
        """ Return default
        """
        return (
            self.view_accessor('operation'),
            self.view_accessor('value'),
            self.view_accessor('daterange'),
        )

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
            operation, value, daterange = value
            operation = operation()
            value = value()
            daterange = daterange()
        else:
            form_value = form.get(self.data.getId(), ())
            if not form_value or len(form_value)!=3:
                return query
            operation, value, daterange = form_value

        try:
            operation = operation.lower()
            assert(operation in ['', 'equal', 'more', 'less'])
            value = int(value or 0)
            daterange = str(daterange)
            assert(daterange in ['', 'past', 'future'])
        except Exception, err:
            logger.exception(err)
            return query

        # Negate the value for 'old' days
        if daterange == 'past':
            value = -value

        date = DateTime() + value
        current_date = DateTime()

        if operation == 'equal':
            date_range = (date.earliestTime(), date.latestTime())
            query[index] = {'query': date_range, 'range': 'min:max'}
        elif operation == 'more':
            if value != 0:
                range_op = (daterange == 'past' and 'max') or 'min'
                query[index] = {'query': date.earliestTime(), 'range': range_op}
            else:
                query[index] = {'query': date, 'range': 'min'}
        elif operation == 'less':
            if value != 0:
                date_range = (daterange == 'past' and (date.earliestTime(), current_date)
                              ) or (current_date, date.latestTime())

                query[index] = {'query': date_range, 'range': 'min:max'}
            else:
                query[index] = {'query': date, 'range': 'max'}
        return query
