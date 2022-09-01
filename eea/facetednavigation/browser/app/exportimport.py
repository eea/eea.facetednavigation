""" Export / Import faceted configuration
"""
from eea.facetednavigation import _
from plone.protect.interfaces import IDisableCSRFProtection
from Products.GenericSetup.context import SnapshotExportContext
from Products.GenericSetup.context import SnapshotImportContext
from Products.GenericSetup.interfaces import IBody
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides


class FacetedExportImport(object):
    """Faceted view"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # XXX Quick fix until we figure out how to enable CSRF Protection
        alsoProvides(request, IDisableCSRFProtection)

    def _redirect(self, msg="", to="configure_faceted.html"):
        """Set status message and redirect"""
        if not to:
            return msg

        if msg:
            IStatusMessage(self.request).addStatusMessage(str(msg), type="info")
        self.request.response.redirect(to)

    def _import_xml(self, **kwargs):
        """Import"""
        upload_file = kwargs.get("import_file", None)
        if getattr(upload_file, "read", None):
            upload_file = upload_file.read()
        xml = upload_file or b""
        if not xml.startswith(b'<?xml version="1.0"'):
            return _("Please provide a valid xml file")

        environ = SnapshotImportContext(self.context, "utf-8")
        importer = queryMultiAdapter((self.context, environ), IBody)
        if not importer:
            return "No adapter found"

        try:
            importer.body = xml
        except Exception as err:
            return "ERROR: %s" % err
        else:
            return _("Configuration imported")

    def import_xml(self, **kwargs):
        """Import config from xml"""
        msg = self._import_xml(**kwargs)
        return self._redirect(msg, kwargs.get("redirect", "configure_faceted.html"))

    def _export_xml(self, **kwargs):
        """Export"""
        environ = SnapshotExportContext(self.context, "utf-8")
        return queryMultiAdapter((self.context, environ), IBody)

    def export_xml(self, **kwargs):
        """Export config as xml"""
        exporter = self._export_xml(**kwargs)
        if not exporter:
            return self._redirect(
                "No adapter found", kwargs.get("redirect", "configure_faceted.html")
            )

        self.request.response.setHeader("content-type", "text/xml; charset=utf-8")
        self.request.response.addHeader(
            "content-disposition",
            "attachment; filename=%s.xml" % (self.context.getId(),),
        )
        return exporter.body

    def __call__(self, **kwargs):
        """Export / Import configuration"""
        if self.request:
            kwargs.update(self.request.form)
        if "import_button" in kwargs.keys():
            return self.import_xml(**kwargs)
        if "export_button" in kwargs.keys():
            return self.export_xml(**kwargs)
        self._redirect(_("No action provided"), "configure_faceted.html")
