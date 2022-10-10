""" Utils
"""

from zope.i18n import translate

import time


LANGUAGES = (
    "af",
    "ar",
    "az",
    "bg",
    "bs",
    "ca",
    "cs",
    "da",
    "de",
    "el",
    "en-GB",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fr-CH",
    "fr",
    "he",
    "hr",
    "hu",
    "hy",
    "id",
    "is",
    "it",
    "ja",
    "ko",
    "lt",
    "lv",
    "ms",
    "nl",
    "no",
    "pl",
    "pt-BR",
    "ro",
    "ru",
    "sk",
    "sl",
    "sq",
    "sr",
    "sr-SR",
    "sv",
    "th",
    "tr",
    "uk",
    "vi",
    "zh-CN",
    "zh-HK",
    "zh-TW",
)


def get_datepicker_date_format(request):
    """Return a localized date format we can use with the datepicker
    jqueryui plugin. The date format is retrieved from the
    date_format_short_datepicker msgid in the plonelocales i18n domain.
    Return 'mm/dd/yy' if no translation has been found.
    """
    date_format = translate(
        "date_format_short_datepicker", domain="plonelocales", context=request
    )
    if date_format == "date_format_short_datepicker":
        return "mm/dd/yy"
    return date_format


def transform_to_percent(date_format):
    """Transform a jquery `date_format` to a date format that time.strptime
    understand. Replace "mm" by "%m", "dd" by "%d", and "yy" by "%Y".

    >>> transform_to_percent("mm/dd/yy")
    '%m/%d/%Y'
    >>> transform_to_percent("dd/mm/yy")
    '%d/%m/%Y'
    >>> transform_to_percent("yy/mm/dd")
    '%Y/%m/%d'
    >>> transform_to_percent("yy-mm-dd")
    '%Y-%m-%d'
    >>> transform_to_percent("dd.mm.yy")
    '%d.%m.%Y'
    >>> transform_to_percent("dd.mm.yy.")
    '%d.%m.%Y.'
    >>> transform_to_percent("yy.mm.dd.")
    '%Y.%m.%d.'
    """
    return date_format.replace("mm", "%m").replace("dd", "%d").replace("yy", "%Y")


def get_python_date_format(request):
    return transform_to_percent(get_datepicker_date_format(request))


def parse_date(datestr, date_format):
    """Parse datestr given the date_format and return a tuple
    (year, month, day)

    >>> date = parse_date("17.03.2010", "%d.%m.%Y")
    >>> date
    (2010, 3, 17)

    And you can after that create a datetime object like this:

    >>> import datetime
    >>> datetime.date(*date)
    datetime.date(2010, 3, 17)
    """
    return time.strptime(datestr, date_format)[:3]
