""" Custom Archetypes fields
"""
from zope import component
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.Archetypes.Field import StringField as ArchStringField
from Products.Archetypes.utils import DisplayList

class StringField(ArchStringField):
    """ Override Vocabulary method to accept zope3 like vocabularies
    """
    def Vocabulary(self, content_instance=None):
        """ Override Vocabulary method (copied from plone 3)
        """
        value = self.vocabulary

        if value:
            return ArchStringField.Vocabulary(self, content_instance)

        factory_name = getattr(self, 'vocabulary_factory', None)
        if not factory_name:
            return ArchStringField.Vocabulary(self, content_instance)

        factory = component.getUtility(IVocabularyFactory, name=factory_name)
        factory_context = content_instance
        if factory_context is None:
            factory_context = self
        self.vocabulary = DisplayList([(t.value, t.title or t.token)
                                       for t in factory(factory_context)])

        return ArchStringField.Vocabulary(self, content_instance)
