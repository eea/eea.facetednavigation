""" Adapters
"""
import logging
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.indexes.language.interfaces import (
    ILanguageWidgetAdapter,
)
logger = logging.getLogger('eea.facetednavigation.language')


@implementer(ILanguageWidgetAdapter)
class LanguageWidgetAdapter(object):
    """ Handler for language widgets
    """
    def __init__(self, widget, context):
        self.widget = widget
        self.context = context

    @property
    def default(self):
        """ Override default widget value
        """
        if self.widget.data.get('default', ''):
            return self.language
        return ''

    @property
    def all_languages(self):
        """ Return all available languages
        """
        codes = []
        ltool = getToolByName(self.context, 'portal_languages', None)
        if ltool is not None:
            lang = ltool.getAvailableLanguages()
            codes = lang.keys()
            codes.append('')
        return codes

    @property
    def language(self):
        """ Get context language
        """
        try:
            lang = self.context.getLanguage()
        except AttributeError:
            lang = ''
        return lang or self.context.REQUEST.get('LANGUAGE', '')

    def __call__(self, form):
        """
        """
        logger.debug(form)

        # Counting results per language
        if form.get('_language_count_', False):
            return {'Language': self.all_languages}

        # Global settings
        if self.widget.hidden:
            if not self.widget.default:
                # "All" languages
                return {'Language': self.all_languages}
            else:
                # Context or Session language
                return {'Language': self.language}

        # Non AJAX call
        if not form.get('ajax', True):
            return {}

        query = self.widget.query(form)
        lang = query.get('Language', '')
        if isinstance(lang, dict):
            lang = lang.get('query', '')

        # All languages
        if not lang:
            return {'Language': self.all_languages}

        return query
