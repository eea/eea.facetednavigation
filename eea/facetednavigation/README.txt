EEA Faceted Navigation

  Faceted navigation is a revolutionary plone package that redefines search
  and navigation within plone sites.
  "Project site", http://svn.eionet.europa.eu/projects/Zope/wiki/FacetedNavigation

  Requires

    * "eea.jquery", http://eggrepo.eea.europa.eu/simple

    * "eea.faceted.vocabularies", http://eggrepo.eea.europa.eu/simple

    * "simplejson", http://pypi.python.org/pypi/simplejson/2.0.9

    * "p4a.common", http://pypi.python.org/pypi/p4a.common/1.0.5

    * "p4a.z2utils", http://pypi.python.org/pypi/p4a.z2utils/1.0.2

    * "p4a.subtyper", http://pypi.python.org/pypi/p4a.subtyper/1.1.1

    * "Plone 2.5", http://launchpad.net/plone/2.5/2.5.5 (fully supported)

      - "CMFonFive", http://codespeak.net/svn/z3/CMFonFive/trunk

      - "Five", http://svn.zope.org/repos/main/Products.Five/branches/1.4

      - "FiveSite", http://svn.eionet.europa.eu/repositories/Zope/trunk/FiveSite

    * "Plone 3.3", https://launchpad.net/plone/3.3/3.3.1 (fully supported)

  Optional

    * Customized vocabularies

      - Plone 2.5

        - "ATVocabularyManager", http://plone.org/products/atvocabularymanager/releases/1.3rc1/atvocabularymanager-1-3rc1.tgz

      - Plone 3.3

        - "Products.ATVocabularyManager-1.4.2", http://pypi.python.org/pypi/Products.ATVocabularyManager/1.4.2

    * Multilingual/translation solution

      - Plone 2.5

        - "LinguaPlone", http://svn.plone.org/svn/plone/LinguaPlone/branches/plone-2.5-compatible

      - Plone 3.3

        - "Products.LinguaPlone-2.4", http://pypi.python.org/pypi/Products.LinguaPlone/2.4

    * Syndication

      - "Products.basesyndication", http://svn.plone.org/svn/collective/Products.basesyndication/trunk

      - "Products.fatsyndication", http://svn.plone.org/svn/collective/Products.fatsyndication/trunk

      - "bda.feed", http://svn.plone.org/svn/collective/bda.feed/trunk

    * Cache (memcache)

      - "plone.memoize", http://pypi.python.org/pypi/plone.memoize

      - "lovely.memcached", http://pypi.python.org/pypi/lovely.memcached

      - 'eea.cache', http://eggrepo.eea.europa.eu/simple

    * Extended functionality

      - "eea.faceted.tool", http://eggrepo.eea.europa.eu/simple

  Install

    1. with zc.buildout

      * buildout.cfg should look like::

        ...
        find-links =
            ...
            http://eggrepo.eea.europa.eu/simple
            ...

        ...

        eggs =
          ...
          eea.facetednavigation
          eea.faceted.tool                      (Optional)
          ...

        [instance]

        ...

        zcml =
            eea.facetednavigation-meta
            eea.facetednavigation-overrides
            eea.facetednavigation
            eea.faceted.tool                    (Optional)

    2. without zc.buildout

      * Create a file called **001-eea.facetednavigation-meta.zcml** in the
        **/path/to/instance/etc/package-includes** directory.  The file
        should only contain this::

        <include package="eea.facetednavigation" file="meta.zcml" />

      * Create a file called **002-eea.facetednavigation-overrides.zcml** in the
        **/path/to/instance/etc/package-includes** directory.  The file
        should only contain this::

        <include package="eea.facetednavigation" file="overrides.zcml" />

      * Create a file called **003-eea.facetednavigation-configure.zcml** in the
        **/path/to/instance/etc/package-includes** directory.  The file
        should only contain this::

        <include package="eea.facetednavigation" file="configure.zcml" />

    3. use the QuickInstaller to add this product to your Plone site or using
      portal_setup import profile EEA Faceted Navigation.
      Optional you can install **EEA Faceted Tool** product.

Documentation

  See the **docs** directory in this package.

Authors and contributors

  * "Alin Voinea", mailto:alin.voinea@eaudeweb.ro

  * "Antonio De Marinis", mailto:antonio.de.marinis@eea.europa.eu

  * "Alec Ghica", mailto:alec.ghica@eaudeweb.ro

Credits

  "Izhar Firdaus", mailto:kagesenshi.87@gmail.com for:

      * making faceted navigation aware of collection's query;

      * replacing portal_fiveactions with portal_actions as it caused
        conflict with p4a.plonecalendar and p4a.video
