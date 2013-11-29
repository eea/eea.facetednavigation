#coding=utf-8

import pkg_resources
try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    def normalize(value):
        if isinstance(value, unicode):
            return value.encode('utf-8')
        else:
            return value
else:
    def normalize(value):
        if isinstance(value, str):
            return value.decode('utf-8')
        else:
            return value
