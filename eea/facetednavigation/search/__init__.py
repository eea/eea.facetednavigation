""" Search
"""
try:
    from plone.app.querystring import queryparser
    parseFormquery = queryparser.parseFormquery
except (ImportError, AttributeError):
    def parseFormquery(*args, **kwargs):
        """ plone.app.querystring not installed
        """
        return {}
