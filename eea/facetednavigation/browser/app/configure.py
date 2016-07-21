""" Faceted configure
"""
import logging
from zope.interface import implementer, alsoProvides
from zope.event import notify
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from eea.facetednavigation.plonex import IDisableCSRFProtection
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


@implementer(interfaces.IFacetedCriteriaHandler)
class FacetedCriteriaHandler(FacetedBasicHandler):
    """ Edit criteria
    """
    def add(self, **kwargs):
        """ See IFacetedCriteriaHandler
        """
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
        to_delete = kwargs.get('paths', kwargs.get('ids', ()))
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_update_criterion')
        for cid in to_delete:
            handler.delete(cid)
        return self._redirect(_(u"Filters deleted"), to=self.redirect)


@implementer(interfaces.IFacetedCriterionHandler)
class FacetedCriterionHandler(FacetedBasicHandler):
    """ Edit criterion
    """
    def extractData(self, widget, **kwargs):
        """ Extract form
        """
        widget.update()
        form, _errors = widget.extractData()
        form.update(kwargs)
        return form

    def add(self, **kwargs):
        """ See IFacetedCriterionHandler
        """
        wid = kwargs.pop('wtype',
                         self.request.get('wtype', None))
        position = kwargs.pop('wposition',
                              self.request.get('wposition', 'right'))
        section = kwargs.pop('wsection',
                             self.request.get('wsection', 'default'))

        criteria = ICriteria(self.context)
        cid = criteria.add(wid, position, section)
        return self.edit(cid, __new__=True, **kwargs)

    def edit(self, cid, **kwargs):
        """ See IFacetedCriterionHandler
        """
        criteria = ICriteria(self.context)
        widget = criteria.widget(cid=cid)
        criterion = criteria.get(cid)
        if kwargs.pop('__new__', False):
            criterion = criterion.__class__(cid='c0')
        widget = widget(self.context, self.request, criterion)

        wid = kwargs.pop('widget', None)
        properties = self.extractData(widget, **kwargs)
        if wid:
            properties['widget'] = wid

        update = {}
        for prop, value in properties.items():
            form_key =  'faceted.%s.%s' % (cid, prop)
            if form_key not in kwargs and value is None:
                continue
            update[prop] = value

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


@implementer(interfaces.IFacetedPositionHandler)
class FacetedPositionHandler(FacetedBasicHandler):
    """ Edit criteria position
    """
    def update(self, **kwargs):
        """ Update position by given slots
        """
        logger.debug(kwargs)
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


@implementer(interfaces.IFacetedFormHandler)
class FacetedFormHandler(FacetedBasicHandler):
    """ Edit criteria using a static form
    """
    def __init__(self, context, request):
        super(FacetedFormHandler, self).__init__(context, request)
        # XXX Quick fix until we figure out how to enable CSRF Protection
        alsoProvides(request, IDisableCSRFProtection)

    def __call__(self, **kwargs):
        """ This method is called from a form with more than one submit buttons
        """
        sanitized_form = {}
        for key, value in getattr(self.request, 'form', {}).items():
            key = key.replace('[]', '')
            if isinstance(value, str):
                value = value.decode('utf-8')
            sanitized_form[key] = value

        if sanitized_form:
            self.request.form = sanitized_form
            kwargs.update(sanitized_form)
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
        if kwargs.pop('addPropertiesWidget_button', None):
            return handler.add(**kwargs)

        # Delete button clicked
        if kwargs.pop('deleteWidget_button', None):
            cid = kwargs.pop('path', kwargs.pop('cid', ''))
            return handler.delete(cid=cid, **kwargs)

        # Save button clicked
        if kwargs.pop('updateCriterion_button', None):
            return handler.edit(**kwargs)
        #
        # Position
        #
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_update_position')

        # Update position
        if kwargs.get('updatePosition_button', None):
            return handler.update(**kwargs)

        # Move up button clicked
        move_up = [k for k in kwargs
                   if k.startswith('moveUp_button')]
        if move_up:
            cid = move_up[0].split('+++')[1]
            return handler.move_up(cid)

        # Move down button clicked
        move_down = [k for k in kwargs
                   if k.startswith('moveDown_button')]
        if move_down:
            cid = move_down[0].split('+++')[1]
            return handler.move_down(cid)

        # Return
        self._redirect('Nothing changed', to=self.redirect)


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
