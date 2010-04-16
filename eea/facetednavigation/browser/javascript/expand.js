var FacetedExpand = {version: '2.0'};

FacetedExpand.ExpandColapse = function(wid, container){
  var hideitems = jQuery('li.faceted-maxitems-hide', container);

  // More
  var more = jQuery('<div>');
  more.addClass('faceted-checkbox-more');
  var mlink = jQuery('<a>');
  mlink.attr('href', '#');
  mlink.html('More');
  more.html(mlink);
  more.hide();
  container.append(more);

  // Less
  var less = jQuery('<div>');
  less.addClass('faceted-checkbox-less');
  var llink = jQuery('<a>');
  llink.attr('href', '#');
  llink.html('Less');
  less.html(llink);
  less.hide();
  container.append(less);

  more.click(function(){
    hideitems.show();
    more.hide();
    less.show();
    return false;
  });

  less.click(function(){
    hideitems.hide();
    less.hide();
    more.show();
    scroll(0, 0);
    return false;
  });

  if(hideitems.length){
    less.click();
  }
};
