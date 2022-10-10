""" Test utilities
"""
from io import BytesIO

import os


def loadfile(rel_filename):
    """Open a file relative to this module"""
    storage_path = os.path.join(os.path.dirname(__file__))
    file_path = os.path.join(storage_path, rel_filename)

    filename = filedata = ""
    with open(file_path, "rb") as file_ob:
        filedata = file_ob.read()
        filename = file_path.split("/")[-1]
        filename = str(filename)

    return {
        "name": filename,
        "data": filedata,
    }


def preparefile(rel_filename, ctype="text/xml"):
    """Prepare a file for upload"""
    ofile = loadfile(rel_filename)
    fp = BytesIO(ofile.get("data"))
    fp.filename = ofile.get("name")
    return fp


class DummySolrResponse(dict):
    """Solr"""

    @property
    def facet_counts(self):
        """Count"""
        return {"facet_fields": self}
