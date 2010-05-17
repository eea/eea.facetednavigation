""" Faceted navigation permissions
"""
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

security = ModuleSecurityInfo('eea.facetednavigation.permissions')

security.declarePublic('ConfigureFaceted')
ConfigureFaceted = 'eea.facetednavigation : Configure faceted'
setDefaultRoles( ConfigureFaceted, ('Manager','Owner'))
