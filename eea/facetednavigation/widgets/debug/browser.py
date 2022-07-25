""" Debug widget support
"""
from pprint import pformat
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.widgets.debug.widget import Widget

from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IWidgetFilterBrains
from eea.facetednavigation.widgets.widget import CountableWidget

class Debug(BrowserView):
    """ Query debugger util views
    """
    def visible(self, **kwargs):
        """ Visibility
        """
        if self.request:
            kwargs.update(self.request.form)

        cid = kwargs.get('debugger', None)
        if not cid:
            return False

        criteria = queryAdapter(self.context, ICriteria)
        if not criteria:
            return False

        criterion = criteria.get(cid)
        if not criterion:
            return False

        wtype = criterion.get('widget')
        if wtype != Widget.widget_type:
            return False

        mtool = getToolByName(self.context, 'portal_membership')
        user = mtool.getAuthenticatedMember()
        allowed = criterion.get('user', u'DEBUGGER USER NOT SET')
        if allowed != user.getId():
            return False

        return True

    def query(self, **kwargs):
        """ Return current faceted query
        """
        if self.request:
            kwargs.update(self.request.form)

        if not self.visible(**kwargs):
            return "[]"

        view = queryMultiAdapter((self.context, self.request),
                                 name=u'faceted_query')
        if not view:
            return "[]"

        query = view.criteria(**kwargs)
        return pformat(query)

    def after(self, **kwargs):
        """ After query filters
        """
        if self.request:
            kwargs.update(self.request.form)

        mode = kwargs.get('mode', 'view')
        if not self.visible(**kwargs):
            return "[]"

        criteria = queryAdapter(self.context, ICriteria)
        res = []
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)
            widget = widget(self.context, self.request, criterion)

            aquery = queryAdapter(widget, IWidgetFilterBrains)
            if not aquery:
                continue

            rep = {}
            rep['handler'] = '.'.join((
                    aquery.__module__, aquery.__class__.__name__))
            rep['index'] = criterion.get('index', None)
            rep['title'] = criterion.get('title', None)
            rep['widget'] = criterion.get('widget', None)

            if mode == 'edit':
                if not widget.hidden:
                    continue
                rep['default'] = widget.default
            elif mode == 'view':
                if widget.hidden:
                    rep['default'] = widget.default
                else:
                    value = kwargs.get(cid, None)
                    if not value:
                        continue
                    rep['value'] = value

            res.append(rep)
        if not res:
            return "[]"
        return pformat(res)

    def counters(self, **kwargs):
        """ Return current counters
        """
        if self.request:
            kwargs.update(self.request.form)

        if not self.visible(**kwargs):
            return "[]"

        handler = queryMultiAdapter((self.context, self.request),
                                    name=u'faceted_query')

        criteria = queryAdapter(self.context, ICriteria)
        res = []
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)
            widget = widget(self.context, self.request, criterion)

            if not isinstance(widget, CountableWidget):
                continue

            if widget.hidden:
                continue

            if not widget.countable:
                continue

            rep = {}
            props = kwargs.copy()
            props.pop(cid, None)
            title = criterion.get('title', None) or criterion.getId()
            rep[title] = handler.criteria(sort=False, **props)
            res.append(rep)

        if not res:
            return "[]"
        return pformat(res)

    def criteria(self, **kwargs):
        """ Return current criteria
        """
        if self.request:
            kwargs.update(self.request.form)

        if not self.visible(**kwargs):
            return "[]"

        mode = kwargs.get('mode', 'view')
        if mode == 'view':
            return "[]"

        criteria = queryAdapter(self.context, ICriteria)
        res = []
        for cid, criterion in criteria.items():
            widget = criteria.widget(cid=cid)

            rep = criterion.__dict__.copy()
            rep['class'] = '.'.join((widget.__module__, widget.__name__))
            res.append(rep)
        return pformat(res)
