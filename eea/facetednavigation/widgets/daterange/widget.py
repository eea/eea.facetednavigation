""" Text widget
"""
import logging

from DateTime import DateTime
from datetime import datetime

from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import SelectionWidget

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _


logger = logging.getLogger('eea.facetednavigation.widgets.daterange')

def formated_time(datestr):
    """Return a DateTime object from a string with
    Y-m-d as format."""
    try:
        if(len(datestr) <= 4):
            datestr = datetime.strptime(datestr, '%Y')
        elif '-' in datestr:
            datestr = datetime.strptime(datestr, '%Y-%m-%d')
        elif '/' in datestr:
            datestr = datetime.strptime(datestr, '%Y/%m/%d')
    except Exception, err:
        logger.warn(err)
    return DateTime(datestr)

EditSchema = Schema((
    StringField('index',
        schemata="default",
        required=True,
        vocabulary_factory='eea.faceted.vocabularies.DateRangeCatalogIndexes',
        widget=SelectionWidget(
            format='select',
            label=_(u'Catalog index'),
            description=_(u'Catalog index to use for search'),
            i18n_domain="eea"
        )
    ),
    StringField('default',
        schemata="default",
        widget=StringWidget(
            size=25,
            label=_(u'Default value'),
            description=_(u"Default daterange (e.g. '2009/12/01=>2009/12/31')"),
            i18n_domain="eea"
        )
    ),
    StringField('calYearRange',
        schemata="display",
        default="c-10:c+10",
        widget=StringWidget(
            size=25,
            label=_(u'UI Calendar years range'),
            description=_(u'Control the range of years'
                          'displayed in the year drop-down: '
                          'either relative to today\'s year '
                          '(-nn:+nn), relative to the '
                          'currently selected year (c-nn:c+nn'
                          '), absolute (nnnn:nnnn), or '
                          'combinations of these formats '
                          '(nnnn:-nn).'),
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
        start, end = start.replace('/', '-'), end.replace('/', '-')
        # be sure years are 0padded & 4 digits
        # this to allow very old years to be entered up
        bounds = {'start': start, 'end': end}
        for sbound in bounds:
            bound = bounds[sbound]
            parts = bound.split('-')
            if len(parts) == 3:
                year, month, day = parts
                ypadding = 4 - len(year)
                mpadding = 2 - len(month)
                dpadding = 2 - len(day)
                bounds[sbound] = '%s-%s-%s'% (
                    '0'* ypadding + year,
                    '0'* mpadding + month,
                    '0'* dpadding + day,)

        start, end = bounds['start'], bounds['end']

        if not (start and end):
            return query


        try:
            # give datetime.datetime to allow very old or big years
            # not to be transformed in current years (eg: 0001 -> 1901)
            start = formated_time(start)
            end = formated_time(end)
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


    @property
    def cal_year_range(self):
        """Return the stored value of calYearRange."""
        return self.accessor('calYearRange')()

