""" SKOS
"""
from zope.component import getMultiAdapter

class SKOS(object):
    """ Browser view for generating a SKOS feed from a
        Faceted Navigable container.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def concepts(self):
        """ SKOS concepts
        """
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_query')
        brains = handler.query(ajax=False)
        for brain in brains:
            doc = brain.getObject()
            if not doc or not hasattr(doc, 'getTranslations'):
                continue

            languages = doc.getTranslations()
            prefLabels = []
            for lang, doc_list in languages.items():
                prefLabel = {
                    'language': lang,
                    'title': doc_list[0].Title()
                }
                prefLabels.append(prefLabel)

            yield {
                'url': doc.absolute_url(),
                'prefLabels': prefLabels,
                'definition': doc.Description()
            }
