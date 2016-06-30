""" Widget
"""
import logging
from DateTime import DateTime

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation.widgets.date.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.date.interfaces import LayoutSchemata
from eea.facetednavigation import EEAMessageFactory as _

logger = logging.getLogger('eea.facetednavigation.widgets.daterange')

PAST = (
    (730, _('2 years ago')),
    (365, _('1 year ago')),
    (186, _('6 months ago')),
    (93, _('3 months ago')),
    (31, _('1 month ago')),
    (14, _('2 weeks ago')),
    (7, _('1 week ago')),
    (5, _('5 days ago')),
    (2, _('2 days ago')),
    (1, _('Yesterday'))
)

FUTURE = (
    (1, _('Tomorrow')),
    (2, _('Next 2 days')),
    (5, _('Next 5 days')),
    (7, _('Next week')),
    (14, _('Next 2 weeks')),
    (31, _('Next month')),
    (93, _('Next 3 months')),
    (186, _('Next 6 months')),
    (365, _('Next year')),
    (730, _('Next 2 years')),
)


class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'date'
    widget_label = _('Date')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Return default value
        """
        default = self.data.get('default', '')
        if not default:
            return ('now-past', 'now_future')

        default = default.split('=>')
        if len(default) == 1:
            return ('now-past', 'now_future')
        elif len(default) == 2:
            date_from = default[0].strip()
            if not date_from.startswith('now'):
                return ('now-past', 'now_future')
            date_to = default[1].strip()
            if not date_to.startswith('now'):
                return ('now-past', 'now_future')
            return (date_from, date_to)
        return ('now-past', 'now_future')

    @property
    def select_vocabulary(self):
        """ Select vocabulary
        """
        # Past
        res = [
            ('now-past', self.translate(_('Past'))),
        ]
        for key, value in PAST:
            key = 'now-%d' % key
            res.append((key, self.translate(value)))

        # Present
        res.append(('now-0', self.translate(_('Today'))))

        #Future
        for key, value in FUTURE:
            key = 'now_%d' % key
            res.append((key, self.translate(value)))
        res.append(('now_future', self.translate(_('Future'))))
        return res

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
        else:
            value = form.get(self.data.getId(), ())

        if len(value) != 2:
            return query

        from_val, to_val = value

        from_val = from_val.replace('now', '', 1)
        if from_val.startswith('+') or from_val.startswith('_'):
            from_val = from_val[1:]

        to_val = to_val.replace('now', '', 1)
        if to_val.startswith('+') or to_val.startswith('_'):
            to_val = to_val[1:]

        # Empty query
        if from_val == '-past' and to_val == 'future':
            return query

        now = DateTime()
        from_date = DateTime('1970/01/01')
        to_date = DateTime('2030/12/31')

        query_range = 'min:max'

        if from_val == '-past':
            query_range = 'max'
        elif from_val == 'future':
            from_date = DateTime('2030/12/31')
            query_range = 'max'
        else:
            try:
                from_delta = int(from_val)
            except (ValueError, TypeError), err:
                logger.exception(err)
            else:
                from_date = now + from_delta

        if to_val == '-past':
            query_range = 'min'
            to_date = DateTime('1970/01/01')
        elif to_val == 'future':
            query_range = 'min'
        else:
            try:
                to_delta = int(to_val)
            except (ValueError, TypeError), err:
                logger.exception(err)
            else:
                to_date = now + to_delta

        if from_date == to_date:
            date_range = (from_date.earliestTime(), from_date.latestTime())
            query[index] = {'query': date_range, 'range': 'min:max'}
            return query

        if query_range == 'min':
            query[index] = {'query': from_date, 'range': 'min'}
        elif query_range == 'max':
            query[index] = {'query': to_date, 'range': 'max'}
        else:
            query[index] = {'query': (from_date, to_date), 'range': 'min:max'}

        return query
