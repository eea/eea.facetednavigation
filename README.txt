EEA Faceted Navigation (FacetedNav)
===================================
The EEA Faceted Navigation **(FacetedNav)** gives you a
**very powerful interface to improve search within large collections of items.**
No programming skills are required by the website manager to configure the
faceted navigation interface, `configuration is done TTW <http://svn.eionet.europa.eu/projects/Zope/attachment/wiki/FacetedNavigationScreenshots/screenshot7.png>`_.
It lets you gradually select and explore different facets (metadata/properties)
of the site content and narrow down you search quickly and dynamically.

On the contrary, plone collections are static, in a way that the site admin
decides the search criteria and the end user is not able to further sort or
filter the presented results.

**FacetedNav is fully customizable**, site admin may decide that some criteria
(facets) must have fixed values while other may be presented as filter options
to the web visitor.

**FacetedNav may very well replace the standard collection content type**, since
it covers same functionality and it adds a lot more features.

**FacetedNav can also be used as an advanced search for your site**.


Contents
========

.. contents::


Main features
=============
It comes with plenty of configuration options and features like:

 1. Easy customizable GUI via drag-n-drop, no restart needed.
 2. Facets can be set to fixed default values and hidden.
 3. Facets can be placed in standard search or extended search panels,
    to not intimidate novice users and have cleaner interface
 4. Facets can be displayed via several widgets like select, radio,
    text input, tag cloud, date range and more
 5. Expandable and collapsible widgets with many values
 6. Automatically counts number of content items beside each facet value
 7. Possibility to show or hide the options with zero results
    (show only the facets which return content)
 8. Ability to create your custom content types definition to be used as a
    combination of interface and portal type, presented in a single widget.
 9. Export of search result in RSS.
 10. Pleasant user interface based on Ajax JQuery, implemented with "deep linking",
     so bookmarking a faceted query works, browser history supported.
 11. Export / Import of faceted settings as XML. Useful to replicate same facets
     navigation on another site.
 12. Search engine friendly, disabling javascript acts as a normal collection
     batch list.
 13. Synchronization of settings across multiple languages, I18N support.
 14. High performance by caching faceted catalog queries via `distributed memory
     object caching system: memcached <http://www.danga.com/memcached/>`_


Extra
=====
You can extend faceted navigation functionality by installing the following
addons:

  - Customized vocabularies
      - Products.ATVocabularyManager

  * Multilingual/translation solution
      - Products.LinguaPlone

  * Syndication
      - Products.basesyndication
      - Products.fatsyndication
      - bda.feed

  * Cache (memcache)
      - plone.memoize
      - lovely.memcached
      - eea.cache

  * Faceted extensions
      - eea.faceted.tool
      - eea.faceted.inheritance

  * Faceted themes
      - eea.faceted.blue


Screenshots
===========
 See more `FacetedNavigationScreenshots <http://svn.eionet.europa.eu/projects/Zope/wiki/FacetedNavigationScreenshots>`_.


Live demo
=========
Here some live production demos:

 - `EEA Publications <http://www.eea.europa.eu/publications>`_
 - `EEA Multimedia <http://www.eea.europa.eu/multimedia>`_
 - `University of Minnesota - Explore Books <http://upress.umn.edu/explore>`_


Buildout installation
=====================
  - Plone 2 and 3
    - Buildouts: http://svn.eionet.europa.eu/repositories/Zope/trunk/eea.facetednavigation/buildouts
    - Trac: http://svn.eionet.europa.eu/projects/Zope/browser/trunk/eea.facetednavigation/buildouts
  - Plone 4+
    - Buildout: http://svn.plone.org/svn/collective/eea.facetednavigation/buildout
    - Trac: http://dev.plone.org/collective/browser/eea.facetednavigation/buildout


Source code
===========
  - Plone 2 and 3:
    - Latest source code in EEA svn: https://svn.eionet.europa.eu/repositories/Zope/trunk/eea.facetednavigation/
  - Plone 4+
    - Collective: https://github.com/collective/eea.facetednavigation


Eggs repository
===============
 - http://eggrepo.eea.europa.eu/simple


Plone versions
==============
It has been developed and tested for Plone 2, 3 and 4. See buildouts section above.


Known bugs and ongoing development
==================================
Bugs and new features are entered on our Trac server at EEA.

  - `open bugs / tasks <http://svn.eionet.europa.eu/projects/Zope/query?status=assigned&status=new&status=reopened&component=Faceted+navigation&order=priority&col=id&col=summary&col=component&col=status&col=type&col=priority&col=milestone>`_
  - `complete list of bugs / features including fixed and open <http://svn.eionet.europa.eu/projects/Zope/query?status=assigned&status=closed&status=new&status=reopened&component=Faceted+navigation&order=priority&col=id&col=summary&col=component&col=status&col=type&col=priority&col=milestone>`_


Copyright and license
=====================
The EEA Faceted Navigation (the Original Code) is free software; you can
redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc., 59
Temple Place, Suite 330, Boston, MA 02111-1307 USA.

The Initial Owner of the Original Code is European Environment Agency (EEA).
Portions created by Eau de Web are Copyright (C) 2009 by
European Environment Agency. All Rights Reserved.


Other resources
===============
 - `Faceted navigation pattern <http://www.welie.com/patterns/showPattern.php?patternID=faceted-navigation>`_
 - `Faceted classification <http://www.webdesignpractices.com/navigation/facets.html>`_
 - `Flamenco faceted navigation <http://flamenco.berkeley.edu/demos.html>`_ made at University of Berkeley
 - `A simpler Faceted plone 3 product made 2008 <http://plone.org/products/faceted-navigation>`_
 - `Folder navigation (GSoC) <http://plone.org/support/forums/core#nabble-td3165375>`_ A new product Folder Navigation in early development]
 - `Exhibit <http://www.simile-widgets.org/exhibit/>`_ Client based faceted navigation via javascript
