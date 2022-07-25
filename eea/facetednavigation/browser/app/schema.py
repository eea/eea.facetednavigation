""" Schema
"""
from eea.facetednavigation.widgets.storage import Criterion
from eea.facetednavigation.widgets.schema import Schema
from eea.facetednavigation.interfaces import ICriteria

class FacetedSchemaGetter(object):
    """ Faceted Query
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_criterion(self, cid):
        """ Criterion
        """
        return ICriteria(self.context).get(cid)

    def get_widget(self, wid):
        """ Widget
        """
        if not wid:
            return None
        return ICriteria(self.context).widget(wid=wid)

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        criterion_id = kwargs.get('criterion', '').split('_')[0]

        criterion = self.get_criterion(criterion_id)
        # Not added yet use an empty one
        if not criterion:
            criterion = Criterion()

        widget_id = kwargs.get('widget', criterion.get('widget', ''))
        widget = self.get_widget(widget_id)
        if not widget:
            return ''

        return Schema(self.context, self.request, widget, criterion)()
