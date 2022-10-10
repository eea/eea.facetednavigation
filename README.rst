======================
EEA Faceted Navigation
======================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.facetednavigation/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.facetednavigation/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.facetednavigation/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.facetednavigation/job/master/display/redirect
  :alt: Master

The EEA Faceted Navigation **(FacetedNav)** gives you a
**very powerful interface to improve search within large collections of items.**
No programming skills are required by the website manager to configure the
faceted navigation interface, configuration is done TTW.
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

**FacetedNav can also be used as an advanced search for your Plone Classic site**.

.. contents::

Upgrade to version 16.0+
========================
* **Version 16.x** is **NOT** backward compatible and **it works only** with **Python 3 / Plone 5+**
* If you're upgrading from a lower version, please first install and upgrade to `version 15.x`` then install and upgrade to `version 16+`
* Upgraded the default faceted view/edit layout to **Bootstrap Grid** and **Bootstrap Card**. Thus, you will need to **adjust your theme** before pushing this version to production.
* Within **Plone > Site setup > Add-ons** click on upgrade button available for `EEA Faceted Navigation`

Upgrade to version 15.0+
========================
* **Version 15.x** is the latest **Python 2 / Plone 4** backward compatible.
* Within "Plone > Site setup > Add-ons" click on upgrade button available for `EEA Faceted Navigation`
* **Plone4:** After running the upgrade step, check CSS/JS order within `ZMI > portal_css / portal_javascript`

Upgrade to version 10.0+
========================
* Within "Plone > Site setup > Add-ons" click on upgrade button available for
  EEA Faceted Navigation;
* Only if the above step didn't work for you. Within "Plone > Site setup > Add-ons"
  uninstall EEA Faceted Navigation and Install it again;
* If you have third-party Faceted Navigation Widgets (registered outside
  eea.facetednavigation package) you will need to upgrade them to z3c.form
  and explicitly register JS/CSS resources within registry.xml/cssregistry.xml/jsregistry,xml
  Take `faceted text widget <https://github.com/collective/eea.facetednavigation/tree/master/eea/facetednavigation/widgets/text>`_  as an example;

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
15. Smart facets hiding - hide facets criteria if there is only one page of
    results (This can be explicitly disabled/enabled from version 4.6.
    It is also disabled by default for new faceted navigable pages starting
    with version 5.2)
16. Ability to transform faceted navigable items in search forms by
    putting them in the 'search mode' (starting with version 4.6)
17. Ability to enable/disable Plone portlets left and right columns within
    faceted navigable contexts (starting with version 4.1. Both disabled by
    default for new faceted navigable pages starting with version 5.2)

Install
=======

* With pip::

    bin/pip install eea.facetednavigation

* Try it with docker::

    docker run --rm -p 8080:8080 -e SITE="Plone" -e ADDONS="eea.facetednavigation" -e PROFILES="eea.facetednavigation:default" plone/plone-backend

* Login to http://localhost:8080/Plone/login (`admin:admin`)
* Install `EEA Faceted Navigation`` via `Site Setup > Add-ons`

Develop
=======

* See `DEVELOP.md <https://github.com/eea/eea.facetednavigation/blob/master/DEVELOP.md>`_

Getting started
===============

* Go to `Site Setup > Content Types` and select `Page`
* Go to `Behaviors` and enable `Faceted navigable` behavior
* Go to your working space and add a `Page` and within `Actions` menu click on `Enable faceted navigation`.

Faceted settings
================

**Faceted settings** is a menu that appears once you enable Faceted navigation
within your context next to the **Actions** menu and it allows you to perform
the following actions:

Configure
---------
Configure Faceted Navigation TTW.

Enable/disable left portlets
----------------------------
This allows you to gain more space for faceted navigation pages by disabling
Plone portlets left column.

Default: **disabled** (*starting with version 5.2*)

Enable/disable right portlets
-----------------------------
This allows you to gain more space for faceted navigation pages by disabling
Plone portlets right column.

Default: **disabled** (*starting with version 5.2*)

Enable/disable smart facets hiding
----------------------------------
Hide facets criteria if there is only one page of results.

Default: **disabled** (*starting with version 5.2*)

Autocomplete widget
===================

Setup
-----

You can enhance and boost search by replacing **ZCatalog** with **Apache Solr**, see `collective.solr`_. Thus:

* Add **collective.solr** to your `requirements.txt` and `constraints.txt`::

    bin/pip install collective.solr

* Start solr::

    $ docker run -p 8983:8983 eeacms/solr

* Install **collective.solr** within **Site Setup > Add-ons**

* **Setup and reindex** Solr within **Site Setup > Solr settings**

* Add or replace **Text** widgets with **Text field with suggestions** within your faceted enabled items.

i18n
----

To include a specific select2 locale, French for instance, just import it to your webpack bundle and make the bundle depend on `plone`::

    import 'select2/select2_locale_fr';


Suggestions
-----------

You can add a new autocomplete source by registering a IAutocompleteSuggest browser view, you can see an example in
`eea/facetednavigation/tests/autocomplete.py <https://github.com/eea/eea.facetednavigation/blob/master/eea/facetednavigation/tests/autocomplete.py>`_ and
`eea/facetednavigation/tests/autocomplete.zcml <https://github.com/eea/eea.facetednavigation/blob/master/eea/facetednavigation/tests/autocomplete.zcml>`_

You also need to configure Solr to include **/suggest** requestHandler. Within your **solrconfig.xml** add::

    <!-- eea.facetednavigation autocomplete -->
    <searchComponent name="suggest" class="solr.SpellCheckComponent">
      <lst name="spellchecker">
        <str name="name">suggest</str>
        <str name="classname">org.apache.solr.spelling.suggest.Suggester</str>
        <str name="lookupImpl">org.apache.solr.spelling.suggest.fst.WFSTLookupFactory</str>
        <str name="field">Title</str>
        <float name="threshold">0.005</float>
        <str name="buildOnCommit">true</str>
      </lst>
    </searchComponent>

    <requestHandler name="/suggest" class="org.apache.solr.handler.component.SearchHandler">
      <lst name="defaults">
        <str name="spellcheck">true</str>
        <str name="spellcheck.dictionary">suggest</str>
        <str name="spellcheck.count">10</str>
        <str name="spellcheck.onlyMorePopular">true</str>
        <str name="wt">xml</str>
      </lst>
      <arr name="components">
        <str>suggest</str>
      </arr>
    </requestHandler>


Extra
=====
You can extend faceted navigation functionality by installing the following add-ons:

* Enhanced text search with autocompletion support

  - `collective.solr`_

* Customized vocabularies

  - `collective.taxonomy <https://github.com/collective/collective.taxonomy>`_
  - `Products.ATVocabularyManager <https://pypi.org/project/Products.ATVocabularyManager>`_ (Plone 4)

* Multilingual/translation solution

  - `plone.app.multilingual <https://pypi.org/project/plone.app.multilingual/>`_
  - `Products.LinguaPlone <https://pypi.org/project/Products.LinguaPlone/>`_ (Plone 3 & 4)

* Cache (memcache)

  - `eea.cache <https://github.com/eea/eea.cache>`_

* Relations

  - `eea.relations <https://pypi.org/project/eea.relations>`_ (Plone 4)

* Extensions

  - `eea.faceted.inheritance <https://pypi.org/project/eea.faceted.inheritance>`_
  - `eea.facetednavigationtaxonomiccheckbox <https://pypi.org/project/eea.facetednavigationtaxonomiccheckbox>`_
  - `collective.eeafaceted.collectionwidget <https://pypi.org/project/collective.eeafaceted.collectionwidget>`_
  - `collective.eeafaceted.layoutwidget <https://pypi.org/project/collective.eeafaceted.layoutwidget>`_
  - `collective.eeafaceted.batchactions <https://pypi.org/project/collective.eeafaceted.batchactions>`_
  - `collective.eeafaceted.dashboard <https://pypi.org/project/collective.eeafaceted.dashboard>`_
  - `collective.eeafaceted.z3ctable <https://pypi.org/project/collective.eeafaceted.z3ctable>`_
  - `collective.faceted.datewidget <https://pypi.org/project/collective.faceted.datewidget/>`_
  - `collective.geo.faceted <https://pypi.org/project/collective.geo.faceted/>`_
  - `collective.contact.facetednav <https://pypi.org/project/collective.contact.facetednav>`_

* Themes

  - `eea.faceted.blue <https://pypi.org/project/eea.faceted.blue/>`_ (Plone 4)

Diazo
=====

To gain performance, you can disable diazo theme on faceted results ajax requests.
Go to "configuration registry" on control panel, select the key "Disable diazo rules on ajax requests"
and set it True. Be sure you do not actually need it.


Live demo
=========

- `EEA Publications <https://www.eea.europa.eu/publications>`_
- `EEA Multimedia <https://www.eea.europa.eu/multimedia/all-videos>`_
- `University of Minnesota - Explore Books <http://upress.umn.edu/explore>`_
- `The Mountaineers <https://mountaineers.org/explore/activities>`_


Source code
===========

- `Plone 2 and 3 on github <https://github.com/eea/eea.facetednavigation/tree/plone3>`_
- `Plone 4 on github <https://github.com/eea/eea.facetednavigation/tree/plone4>`_
- `Plone 5+ on github <https://github.com/eea/eea.facetednavigation>`_


Eggs repository
===============

- https://pypi.python.org/pypi/eea.facetednavigation
- http://eggrepo.eea.europa.eu/simple


Plone versions
==============
It has been developed and tested for Plone `2`, `3`, `4`, `5` and `6`.


How to contribute
=================
See the `contribution guidelines (CONTRIBUTING.md) <https://github.com/eea/eea.facetednavigation/blob/master/CONTRIBUTING.md>`_.

Other resources
===============

- `Faceted navigation pattern <http://www.welie.com/patterns/showPattern.php?patternID=faceted-navigation>`_
- `Exhibit <http://www.simile-widgets.org/exhibit/>`_ Client based faceted navigation via javascript

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


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
.. _`collective.solr`:  https://github.com/collective/collective.solr
