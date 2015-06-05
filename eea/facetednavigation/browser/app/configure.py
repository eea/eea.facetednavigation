""" Faceted configure
"""
import logging
from zope.interface import implements
from zope.event import notify
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from eea.facetednavigation.interfaces import IWidgetsInfo
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.browser import interfaces
from eea.facetednavigation.events import FacetedGlobalSettingsChangedEvent

from eea.facetednavigation import EEAMessageFactory as _


logger = logging.getLogger('eea.facetednavigation.browser.app.configure')
#
# Controllers
#
class FacetedBasicHandler(BrowserView):
    """ Define common methods for criteria handlers
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request or getattr(context, 'request', None)
        self.redirect = context.absolute_url() + '/configure_faceted.html'

    def _redirect(self, msg='', to=''):
        """ Return or redirect
        """
        if not to:
            return msg

        if not self.request:
            return msg

        if msg:
            IStatusMessage(self.request).addStatusMessage(str(msg), type='info')
        self.request.response.redirect(to)
        return msg

    def _request_form(self, form):
        """ Update kwargs from self.request.form
        """
        if getattr(self.request, 'form', None):
            form.update(self.request.form)

        # jQuery >= 1.4 adds type to params keys
        # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
        # Let's fix this
        return dict((key.replace('[]', ''), val)
                    for key, val in form.items())


class FacetedCriteriaHandler(FacetedBasicHandler):
    """ Edit criteria
    """
    implements(interfaces.IFacetedCriteriaHandler)

    def add(self, **kwargs):
        """ See IFacetedCriteriaHandler
        """
        kwargs = self._request_form(kwargs)

        wid = kwargs.pop('wtype', None)
        position = kwargs.pop('wposition', 'right')
        section = kwargs.pop('wsection', 'default')
        try:
            ICriteria(self.context).add(wid, position, section)
        except NameError, err:
            msg = err
        else:
            msg = _(u'Filter added')
        return self._redirect(msg=msg, to=self.redirect)

    def edit(self, **kwargs):
        """ See IFacetedCriteriaHandler
        """
        kwargs = self._request_form(kwargs)

        criteria = ICriteria(self.context)
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_update_criterion')
        for cid in criteria.keys():
            properties = {}
            for key, value in kwargs.items():
                if not key.startswith(cid):
                    continue
                key = key[len(cid) + 1:]
                properties[key] = value
            handler.edit(cid, **properties)
        return self._redirect('Changes saved', to=self.redirect)

    def delete(self, **kwargs):
        """ See IFacetedCriteriaHandler
        """
        kwargs = self._request_form(kwargs)

        to_delete = kwargs.get('paths', kwargs.get('ids', ()))
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_update_criterion')
        for cid in to_delete:
            handler.delete(cid)
        return self._redirect(_(u"Filters deleted"), to=self.redirect)

class FacetedCriterionHandler(FacetedBasicHandler):
    """ Edit criterion
    """
    implements(interfaces.IFacetedCriterionHandler)

    def add(self, **kwargs):
        """ See IFacetedCriterionHandler
        """
        kwargs = self._request_form(kwargs)

        wid = kwargs.pop('wtype', None)
        position = kwargs.pop('wposition', 'right')
        section = kwargs.pop('wsection', 'default')

        criteria = ICriteria(self.context)
        cid = criteria.add(wid, position, section)
        return self.edit(cid, **kwargs)

    def edit(self, cid, **kwargs):
        """ See IFacetedCriterionHandler
        """
        kwargs = self._request_form(kwargs)

        criteria = ICriteria(self.context)
        widget = criteria.widget(cid=cid)
        fields = widget.edit_schema.keys()[:]
        update = {}

        for prop in fields:
            new_value = kwargs.get(prop, None)
            if new_value is None:
                continue
            update[prop] = new_value

        if update:
            criteria.edit(cid, **update)
            if widget.hidden:
                notify(FacetedGlobalSettingsChangedEvent(self.context))
            elif set(['hidden', 'operator']).intersection(update.keys()):
                notify(FacetedGlobalSettingsChangedEvent(self.context))

        return self._redirect('Changes saved')

    def delete(self, cid, **kwargs):
        """ See IFacetedCriterionHandler
        """
        try:
            ICriteria(self.context).delete(cid)
        except (TypeError, KeyError), err:
            msg = err
        else:
            msg = _(u'Filter deleted')
        return self._redirect(msg=msg)

class FacetedPositionHandler(FacetedBasicHandler):
    """ Edit criteria position
    """
    implements(interfaces.IFacetedPositionHandler)

    def _request_form(self, form):
        """ Fix keys
        """
        form = super(FacetedPositionHandler, self)._request_form(form)
        newform = {}
        for key, value in form.items():
            if not value:
                continue
            if isinstance(value, (str, unicode)):
                value = [value]
            newform[key] = value
        return newform

    def update(self, **kwargs):
        """ Update position by given slots
        """
        logger.debug(kwargs)
        kwargs = self._request_form(kwargs)

        ICriteria(self.context).position(**kwargs)
        return self._redirect('Position changed')

    def move_up(self, cid, **kwargs):
        """ Move criterion up
        """
        ICriteria(self.context).up(cid)
        return self._redirect('Position changed', to=self.redirect)

    def move_down(self, cid, **kwargs):
        """ Move criterion down
        """
        ICriteria(self.context).down(cid)
        return self._redirect('Position changed', to=self.redirect)

class FacetedFormHandler(FacetedBasicHandler):
    """ Edit criteria using a static form
    """
    implements(interfaces.IFacetedFormHandler)

    def __call__(self, **kwargs):
        """ This method is called from a form with more than one submit buttons
        """
        kwargs = self._request_form(kwargs)
        #
        # Criteria
        #
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_update_criteria')

        # Add button clicked
        if kwargs.get('addWidget_button', None):
            return handler.add(**kwargs)

        # Delete button clicked
        if kwargs.get('deleteWidgets_button', None):
            return handler.delete(**kwargs)

        # Save button clicked
        if kwargs.get('saveChanges_button', None):
            return handler.edit(**kwargs)
        #
        # Criterion
        #
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_update_criterion')
        # Add button clicked
        if kwargs.get('addPropertiesWidget_button', None):
            properties = {}
            for key, value in kwargs.items():
                key = key.replace('c0_', '', 1)
                properties[key] = value
            return handler.add(**properties)

        # Delete button clicked
        if kwargs.get('deleteWidget_button', None):
            cid = kwargs.pop('path', kwargs.pop('cid', ''))
            return handler.delete(cid=cid, **kwargs)

        # Save button clicked
        if kwargs.get('updateCriterion_button', None):
            cid = kwargs.get('cid', '')
            properties = {}
            for key, value in kwargs.items():
                key = key.replace(cid + '_', '', 1)
                properties[key] = value
            return handler.edit(**properties)
        #
        # Position
        #
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_update_position')

        # Update position
        if kwargs.get('updatePosition_button', None):
            return handler.update(**kwargs)

        # Move up button clicked
        move_up = [k for k in kwargs.keys()
                   if k.startswith('moveUp_button')]
        if move_up:
            cid = move_up[0].split('+++')[1]
            return handler.move_up(cid)

        # Move down button clicked
        move_down = [k for k in kwargs.keys()
                   if k.startswith('moveDown_button')]
        if move_down:
            cid = move_down[0].split('+++')[1]
            return handler.move_down(cid)

        # Return
        self._redirect('Nothing changed', to=self.redirect)
#
# View
#
class FacetedConfigureView(object):
    """ Faceted configure
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def positions(self):
        """ Possible positions
        """
        voc = getUtility(IVocabularyFactory,
                          'eea.faceted.vocabularies.WidgetPositions')
        return voc(self.context)

    @property
    def sections(self):
        """ Possible sections
        """
        voc = getUtility(IVocabularyFactory,
                          'eea.faceted.vocabularies.WidgetSections')
        return voc(self.context)

    def get_widget(self, wid):
        """ Get widget by given widget id
        """
        return ICriteria(self.context).widget(wid)

    def get_widget_types(self):
        """ Widget types
        """
        info = getUtility(IWidgetsInfo)
        res = [x for x in info.widgets.values()]

        def compare(x, y):
            """ Compare """
            return cmp(x.widget_label, y.widget_label)

        res.sort(cmp=compare)
        return res

    def get_schema(self, criterion):
        """ Get edit schema
        """
        schema = getMultiAdapter((self.context, self.request),
                                 name=u'faceted_schema')
        return schema(criterion=criterion.getId())

    def get_criteria(self):
        """ Get criteria
        """
        return ICriteria(self.context).values()
