""" Custom Archetypes fields
"""
from zope import component
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.Archetypes import atapi
from eea.facetednavigation.config import PLONE

class FieldMixin(object):
    """ Override Vocabulary method to accept zope3 like vocabularies
    """
    def Vocabulary(self, content_instance=None):
        """ Override Vocabulary method (copied from plone 3)
        """
        if PLONE >= 3:
            return super(FieldMixin, self).Vocabulary(content_instance)

        factory_name = getattr(self, 'vocabulary_factory', None)
        if not factory_name:
            return super(FieldMixin, self).Vocabulary(content_instance)

        factory = component.getUtility(IVocabularyFactory, name=factory_name)
        factory_context = content_instance
        if factory_context is None:
            factory_context = self
        self.vocabulary = atapi.DisplayList([(t.value, t.title or t.token)
                                       for t in factory(factory_context)])

        return super(FieldMixin, self).Vocabulary(content_instance)

class StringField(FieldMixin, atapi.StringField):
    """ Plone3 like string field
    """
