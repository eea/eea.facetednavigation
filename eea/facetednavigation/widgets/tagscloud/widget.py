""" Tag-Cloud widget
"""
import random
from Products.CMFPlone.utils import safeToInt

from eea.faceted.vocabularies.utils import compare
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.tagscloud.interfaces import DefaultSchemata
from eea.facetednavigation.widgets.tagscloud.interfaces import LayoutSchemata
from eea.facetednavigation.widgets.tagscloud.interfaces import CountableSchemata
from eea.facetednavigation.widgets.tagscloud.interfaces import DisplaySchemata
from eea.facetednavigation.widgets.tagscloud.interfaces import GeometrySchemata
from eea.facetednavigation.widgets.widget import CountableWidget
from eea.facetednavigation import EEAMessageFactory as _


class Widget(CountableWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'tagscloud'
    widget_label = _('Tags Cloud')

    groups = (
        DefaultSchemata,
        LayoutSchemata,
        CountableSchemata,
        DisplaySchemata,
        GeometrySchemata,
    )

    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Get default values
        """
        default = super(Widget, self).default or u''
        return default.encode('utf-8')

    @property
    def maxitems(self):
        """ Maximum items
        """
        return safeToInt(self.data.get('maxitems', 0))

    def cut_text(self, text='', maxchars=0):
        """ Cut long text
        """
        maxchars = safeToInt(self.data.get('maxchars', 0))
        if not maxchars:
            return text

        # Allow 20 % more characters in order
        # to avoid cutting at the end of the text
        if len(text) <= (maxchars + round(0.2 * maxchars)):
            return text
        return '%s...' % text[0:maxchars]

    def vocabulary(self, oll=False, **kwargs):
        """ Return a limited number of results
        """
        voc = list(super(Widget, self).vocabulary())

        if oll:
            maxitems = 0
        else:
            maxitems = self.maxitems

        voc.insert(0, ('all', 'All'))
        for index, item in enumerate(voc):
            if maxitems and (index >= maxitems):
                return
            res = (item[0], item[1], -1)
            yield res

    @property
    def randint(self):
        """ Random integer
        """
        maxint = self.maxitems or 100
        return random.randint(0, maxint)

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
            value = form.get(self.data.getId(), '')
        if not value:
            return query

        if compare(value, 'all') == 0:
            return query

        query[index] = value
        return query

    def __call__(self, **kwargs):
        return self.index(kwargs=kwargs)
