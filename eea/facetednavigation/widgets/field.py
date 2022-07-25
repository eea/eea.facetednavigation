""" Custom Archetypes fields
"""
import warnings
from Products.Archetypes import atapi
StringField = atapi.StringField

warnings.warn("StringField is deprecated. "
              "Please use Archetypes.atapi.StringField instead",
              DeprecationWarning)
