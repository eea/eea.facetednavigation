Plone Faceted Navigation product
================================
A powerful and effective way to find content in large collections

Contents
========

.. contents::


Introduction
============

Faceted Navigation (FN) gives you a very powerful interface to improve
search within large collections of items. It lets you gradually
select and explore different facets (metadata) of the site content and
narrow down you search dynamically.

On the contrary plone collections are static, in a way that the site admin
decide the search criteria and the end user is not able to
further sort or filter the presented results.

FN is fully customizable, site admin may decide that some criteria (facets)
must have fixed values while other may be presented as
filter options to the web visitor.

FN may very well replace the standard collection content type, since it covers
same functionality and it adds a lot more features.


Main features
=============

FN can also be used as an advanced search for your site.
It comes with plenty of configuration options and features like:

   1. Easy customisable GUI via drag-n-drop, no restart needed.
   2. Facets can be set to fixed default values and hidden.
   3. Facets can be placed in standard search or extended
      search panels, to not intimidate novice users and have cleaner interface
   4. Facets can be displayed via several widgets like select,
      radio, text input, tag cloud, date range and more
   5. Expandable and collapsable widgets with many values
   6. Automatically counts number of content items beside each facet value
   7. Possibility to show or hide the options with zero results
      (show only the facets which return content)
   8. Ability to create your custom content types definition to be used
      as a combination of interface and portal type, presented in a single widget.
   9. Export of search result in RSS.
   10. Pleasant user interface based on Ajax JQuery, implemented with "deep linking",
       so bookmarking a faceted query works, browser history supported.
   11. Export / Import of faceted settings as XML. Useful to replicate same facets
       navigation on another site.
   12. Search engine friendly, disabling javascript acts as a normal
       collection batch list.
   13. Synchronisation of settings across multiple languages, I18N support.
   14. High performance by caching faceted catalog queries via distributed
       memory object caching system: memcached

Installation
============

The easiest way to get eea.facetednavigation support in Plone 4 using this
package is to work with installations based on `zc.buildout`_.
Other types of installations should also be possible, but might turn out
to be somewhat tricky.

To get started you will simply need to add the package to your "eggs" and
"zcml" sections, run buildout, restart your Plone instance and install the
"eea.facetednavigation" package using the quick-installer or via the "Add-on
Products" section in "Site Setup".

  .. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout/

You can download a sample buildout at:

  https://svn.plone.org/svn/collective/eea.facetednavigation/buildout

Getting started
===============

Go to the "Actions" tab on a Collection of Folder, and click "enable faceted
navigation".

Dependecies
===========

  1. Plone 4.x


Live demo
=========

Here some live production demos at EEA (European Environment Agency)

   1. EEA Publications http://www.eea.europa.eu/publications
   2. EEA Multimedia http://www.eea.europa.eu/multimedia


Source code
===========

Latest source code (Plone 4 compatible):
   http://svn.plone.org/svn/collective/eea.facetednavigation/trunk

Plone 2 and 3 compatible:
   https://svn.eionet.europa.eu/repositories/Zope/trunk/eea.facetednavigation/


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Faceted Navigation (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

Contributor(s): Alin Voinea (Eau de Web),
                Antonio De Marinis (European Environment Agency),
                Alec Ghica (Eau de Web),
                Sasha Vincic (Valentine Web Systems)
Credits:
                Izhar Firdaus (Inigo Consulting)
                Peter Holzer (Agitator)

More details under docs/License.txt


Links
=====

   1. EEA Faceted Navigation wiki page:
      https://svn.eionet.europa.eu/projects/Zope/wiki/FacetedNavigation


Funding
=======

  EEA_ - European Enviroment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
