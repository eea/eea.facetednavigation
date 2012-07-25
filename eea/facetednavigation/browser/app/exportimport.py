""" Export / Import faceted configuration
"""
from zope.component import queryMultiAdapter
from Products.GenericSetup.interfaces import IBody
from Products.statusmessages.interfaces import IStatusMessage
from Products.GenericSetup.context import SnapshotExportContext
from Products.GenericSetup.context import SnapshotImportContext

from eea.facetednavigation import EEAMessageFactory as _


class FacetedExportImport(object):
    """ Faceted view
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg='', to='configure_faceted.html'):
        """ Set status message and redirect
        """
        if not to:
            return msg

        if msg:
            IStatusMessage(self.request).addStatusMessage(str(msg), type='info')
        self.request.response.redirect(to)

    def import_xml(self, **kwargs):
        """ Import config from xml
        """
        upload_file = kwargs.get('import_file', None)
        if getattr(upload_file, 'read', None):
            upload_file = upload_file.read()
        xml = upload_file or ''
        if not xml.startswith('<?xml version="1.0"'):
            return self._redirect('Please provide a valid xml file',
                kwargs.get('redirect', 'configure_faceted.html'))

        environ = SnapshotImportContext(self.context, 'utf-8')
        importer = queryMultiAdapter((self.context, environ), IBody)
        if not importer:
            return self._redirect('No adapter found',
                kwargs.get('redirect', 'configure_faceted.html'))

        importer.body = xml
        return self._redirect(_(u"Configuration imported"),
                              kwargs.get('redirect', 'configure_faceted.html'))

    def export_xml(self, **kwargs):
        """ Export config as xml
        """
        environ = SnapshotExportContext(self.context, 'utf-8')
        exporter = queryMultiAdapter((self.context, environ), IBody)
        if not exporter:
            return self._redirect('No adapter found',
                kwargs.get('redirect', 'configure_faceted.html'))
        self.request.response.setHeader(
            'content-type', 'text/xml; charset=utf-8')
        self.request.response.addHeader(
            "content-disposition","attachment; filename=%s.xml" % (
                self.context.getId(),))
        return exporter.body

    def __call__(self, **kwargs):
        """ Export / Import configuration
        """
        if self.request:
            kwargs.update(self.request.form)
        if 'import_button' in kwargs.keys():
            return self.import_xml(**kwargs)
        if 'export_button' in kwargs.keys():
            return self.export_xml(**kwargs)
        self._redirect(_(u"No action provided"),
                       'configure_faceted.html')
