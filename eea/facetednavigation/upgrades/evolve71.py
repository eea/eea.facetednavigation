def update_registry(context):
    context.runImportStepFromProfile('profile-eea.facetednavigation:default',
                                     'plone.app.registry', run_dependencies=False,
                                     purge_old=False)