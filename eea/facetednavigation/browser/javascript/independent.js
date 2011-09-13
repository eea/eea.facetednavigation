/*
  Help function which let you have
  normal independent input element sends values to a
  eea.facetednavigation object the correct way.

  How to use it. HTML example:

  <h2>Global search on data and maps</h2>
  <form action="find/global" method="get" class="faceted-external-search">
    <input type="text" name="c12" value="" />
    <input type="submit" value="Go!" name="search" />
  </form>

  c12 = is the parameter id of your text search facet.

*/
jQuery(document).ready(function(){
  jQuery('form.faceted-external-search').submit(function(evt){
    evt.preventDefault();
    var form = jQuery(this);
    var action = form.attr('action');
    var query = form.serialize();
    window.location.href = action + '#' + query;
  });
});
