""" Text widget
"""
import logging
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import IntegerWidget

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
logger = logging.getLogger('eea.facetednavigation.widgets.resultsperpage')

EditSchema = Schema((
    IntegerField('start',
        schemata="display",
        default=0,
        widget=IntegerWidget(
            label='Start',
            label_msgid='faceted_criteria_start',
            description='Results per page starting value',
            description_msgid='help_faceted_criteria_start',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('end',
        schemata="display",
        default=50,
        widget=IntegerWidget(
            label='End',
            label_msgid='faceted_criteria_end',
            description='Results per page ending value',
            description_msgid='help_faceted_criteria_end',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('step',
        schemata="display",
        default=5,
        widget=IntegerWidget(
            label='Step',
            label_msgid='faceted_criteria_step',
            description='Results per page step',
            description_msgid='help_faceted_criteria_step',
            i18n_domain="eea.facetednavigation"
        )
    ),
    IntegerField('default',
        schemata="default",
        default=20,
        widget=IntegerWidget(
            label='Default value',
            label_msgid='faceted_criteria_default',
            description='Default results per page',
            description_msgid='help_faceted_criteria_resultsperpage_default',
            i18n_domain="eea.facetednavigation"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'resultsperpage'
    widget_label = 'Results per page'
    view_js = '++resource++eea.facetednavigation.widgets.resultsperpage.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.resultsperpage.edit.js'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'Results per page'

    @property
    def default(self):
        """ Get default values
        """
        value = self.data.get('default', 0)
        try:
            return int(value)
        except (TypeError, ValueError), err:
            logger.exception(err)
            return 0

    def results_per_page(self, form, default=20):
        """ Get results per page
        """
        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), default)

        if not value:
            return default

        try:
            value = int(value)
        except (TypeError, ValueError), err:
            logger.exception(err)
            return default

        return value

    def vocabulary(self):
        """ Vocabulary
        """
        try:
            start = int(self.data.get('start', 0))
        except (TypeError, ValueError), err:
            logger.exception(err)
            start = 0
        try:
            end = int(self.data.get('end', 21)) + 1
        except (TypeError, ValueError), err:
            logger.exception(err)
            end = 21
        try:
            step = int(self.data.get('step', 1))
        except (TypeError, ValueError), err:
            logger.exception(err)
            step = 1

        return [(x, x) for x in range(start, end, step)]
