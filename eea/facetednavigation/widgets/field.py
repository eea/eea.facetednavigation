""" Custom Archetypes fields
"""
from Products.Archetypes import atapi
StringField = atapi.StringField

import warnings
warnings.warn("StringField is deprecated. "
              "Please use Archetypes.atapi.StringField instead",
              DeprecationWarning)
