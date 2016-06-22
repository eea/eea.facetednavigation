#!/bin/sh
curl -O -k https://bootstrap.pypa.io/bootstrap-buildout.py
chmod u+x bootstrap-buildout.py
virtualenv --no-site-packages .
source bin/activate
bin/python bootstrap-buildout.py
bin/buildout
