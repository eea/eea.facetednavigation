""" Widget
"""
from datetime import datetime
from DateTime import DateTime
from eea.facetednavigation import _
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.daterange.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.daterange.interfaces import DisplaySchemata
from eea.facetednavigation.widgets.daterange.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.daterange.utils import get_datepicker_date_format
from eea.facetednavigation.widgets.daterange.utils import get_python_date_format
from eea.facetednavigation.widgets.daterange.utils import LANGUAGES
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

import logging


logger = logging.getLogger("eea.facetednavigation")


def formated_time(datestr):
    """Return a DateTime object from a string with
    Y-m-d as format."""
    try:
        if len(datestr) <= 4:
            datestr = datetime.strptime(datestr, "%Y")
        elif "-" in datestr:
            datestr = datetime.strptime(datestr, "%Y-%m-%d")
        elif "/" in datestr:
            datestr = datetime.strptime(datestr, "%Y/%m/%d")
    except Exception as err:
        logger.warn(err)
    return DateTime(datestr)


def convert_to_padded_digits(start, end):
    """Be sure years are 0padded & 4 digits
    this to allow very old years to be entered up."""
    start = start.replace("/", "-")
    end = end.replace("/", "-")
    bounds = {"start": start, "end": end}
    for sbound in bounds:
        bound = bounds[sbound]
        parts = bound.split("-")
        if len(parts) == 3:
            year, month, day = parts
            ypadding = 4 - len(year)
            mpadding = 2 - len(month)
            dpadding = 2 - len(day)
            bounds[sbound] = "%s-%s-%s" % (
                "0" * ypadding + year,
                "0" * mpadding + month,
                "0" * dpadding + day,
            )
    return bounds["start"], bounds["end"]


class Widget(AbstractWidget):
    """Widget"""

    widget_type = "daterange"
    widget_label = _("Date range")

    groups = (DefaultSchemata, LayoutSchemata, DisplaySchemata)
    index = ViewPageTemplateFile("widget.pt")

    @property
    def default(self):
        """Return default"""
        default = self.data.get("default", "")
        if not default:
            return "", ""

        default = default.split("=>")
        if len(default) != 2:
            return "", ""

        start, end = default
        start = start.strip()
        end = end.strip()
        if not self.use_plone_date_format:
            start = start.replace("/", "-")
            end = end.replace("/", "-")
        try:
            start = DateTime(datetime.strptime(start, self.python_date_format))
            start = start.strftime(self.python_date_format)
        except Exception as err:
            logger.exception("%s => Start date: %s", err, start)
            start = ""

        try:
            end = DateTime(datetime.strptime(end, self.python_date_format))
            end = end.strftime(self.python_date_format)
        except Exception as err:
            logger.exception("%s => End date: %s", err, end)
            end = ""
        return (start, end)

    def query(self, form):
        """Get value from form and return a catalog dict query"""
        query = {}
        index = self.data.get("index", "")
        if not index:
            return query

        if self.hidden:
            start, end = self.default
        else:
            value = form.get(self.data.getId(), ())
            if not value or len(value) != 2:
                return query
            start, end = value

        if not (start and end):
            return query

        if self.use_plone_date_format:
            try:
                start = DateTime(datetime.strptime(start, self.python_date_format))
                end = DateTime(datetime.strptime(end, self.python_date_format))
            except Exception as err:
                logger.exception(err)
                return query
        else:
            start, end = convert_to_padded_digits(start, end)
            try:
                # give datetime.datetime to allow very old or big years
                # not to be transformed in current years (eg: 0001 -> 1901)
                start = formated_time(start)
                end = formated_time(end)
            except Exception as err:
                logger.exception(err)
                return query

        start = start - 1
        start = start.latestTime()
        end = end.latestTime()

        query[index] = {"query": (start, end), "range": "min:max"}
        return query

    @property
    def cal_year_range(self):
        """Return the stored value of calYearRange."""
        return self.data.get("calYearRange", "c-10:c+10")

    @property
    def use_plone_date_format(self):
        """Return the stored value of usePloneDateFormat."""
        return self.data.get("usePloneDateFormat", False)

    @property
    def js_date_format(self):
        """Return the date format to use with JS datepicker"""
        if self.use_plone_date_format:
            return get_datepicker_date_format(self.request)
        return "yy-mm-dd"

    @property
    def python_date_format(self):
        """Return the date format to use in python"""
        if self.use_plone_date_format:
            return get_python_date_format(self.request)
        return "%Y-%m-%d"

    @property
    def js_language(self):
        """Return the language to use with JS code"""
        if self.use_plone_date_format:
            return self.jq_language()
        return ""

    def jq_language(self):
        language = self.request.get("LANGUAGE", "")
        if "-" in language:
            parts = language.split("-")
            language = "%s-%s" % (parts[0], parts[1].upper())
            if language in LANGUAGES:
                return language
            else:
                language = language.split("-")[0]
        if language in LANGUAGES:
            return language
        return ""
