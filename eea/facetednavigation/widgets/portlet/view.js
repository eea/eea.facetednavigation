Faceted.PortletWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();

  jQuery('legend', this.widget).hide();
  jQuery('fieldset', this.widget).css('border', 'none');

  jQuery('form', this.widget).submit(function(){
    return true;
  });
};

Faceted.initializePortletWidget = function(evt){
  jQuery('div.faceted-portlet-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    var widget = new Faceted.PortletWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializePortletWidget);
});
