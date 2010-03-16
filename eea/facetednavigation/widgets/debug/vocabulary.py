""" Catalog specific vocabularies
"""
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import _getAuthenticatedUser
from Products.Archetypes.public import DisplayList
#
# Object provides
#
class CurrentUserVocabulary(object):
    """Vocabulary factory for logged in user.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """
        user = _getAuthenticatedUser(context)
        user_id = user.getId()
        user_name = user.getUserName()

        return SimpleVocabulary([SimpleTerm(user_id, user_id, user_name)])

CurrentUserVocabularyFactory = CurrentUserVocabulary()
