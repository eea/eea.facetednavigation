##############################################################################
# - Run:
#
#    make
#    make start
#
# - Go to:
#
#     http://localhost:8080
#
# - Create a new Plone Site (admin:admin)
# - Install "EEA Faceted Navigation" via "Site Setup > Add-ons"
# - Add new "Folder" and "Enable Faceted Navigation" from "Actions" menu
#
##############################################################################
# SETUP MAKE
#
## Defensive settings for make: https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
# for Makefile debugging purposes add -x to the .SHELLFLAGS
.SHELLFLAGS:=-eu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# Colors
# OK=Green, warn=yellow, error=red
ifeq ($(TERM),)
# no colors if not in terminal
	MARK_COLOR=
	OK_COLOR=
	WARN_COLOR=
	ERROR_COLOR=
	NO_COLOR=
else
	MARK_COLOR=`tput setaf 6`
	OK_COLOR=`tput setaf 2`
	WARN_COLOR=`tput setaf 3`
	ERROR_COLOR=`tput setaf 1`
	NO_COLOR=`tput sgr0`
endif

##############################################################################
# SETTINGS AND VARIABLE

PLONE_VERSION?=5-latest
PYTHON?=python3.8
PIP_PARAMS=

# Top-level targets
.PHONY: all
all: clean bootstrap install develop

.PHONY: clean
clean:			## Cleanup environment
	rm -rf bin etc include lib lib64 var inituser pyvenv.cfg

.PHONY: bootstrap
bootstrap:		## Bootstrap python environment
	$(PYTHON) -m venv .
	bin/pip install --upgrade pip mxdev pylint black

.PHONY: install
install:		## Install Plone
	bin/pip install Paste Plone plone.volto -c "https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt" $(PIP_PARAMS)
	bin/pip install zope.testrunner plone.app.testing plone.reload dm.plonepatches.reload -c "https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt" $(PIP_PARAMS)
	bin/mkwsgiinstance -d . -u admin:admin
	mkdir -p var/blobstorage var/filestorage

.PHONY: develop
develop:		## Develop this add-on
	bin/pip install -e . $(PIP_PARAMS)

.PHONY: start
start:			## Start Plone backend
	bin/runwsgi -v etc/zope.ini

.PHONY: help
help:			## Show this help.
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"
	head -n 15 Makefile
