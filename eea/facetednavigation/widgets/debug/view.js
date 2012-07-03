/* Debug Widget
*/
Faceted.DebugWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.query_area = jQuery('dd.debug-query pre', this.widget);
  this.after_area = jQuery('dd.debug-after pre', this.widget);
  this.config_area = jQuery('dd.debug-config pre', this.widget);
  this.count_area = jQuery('dd.debug-count pre', this.widget);

  jQuery('dd', this.widget).hide();
  jQuery('dt', this.widget).each(function(){
    var dt = jQuery(this);
    var css = dt.attr('class');
    var parent = dt.parent('dl');
    var minmax = jQuery('<span>').addClass('ui-icon ui-icon-plus').css('float', 'left');
    minmax.click(function(){
      var button = jQuery(this);
      jQuery('dd.' + css, parent).toggle();
      if(button.hasClass('ui-icon-minus')){
        button.removeClass('ui-icon-minus');
        button.addClass('ui-icon-plus');
      }else{
        button.removeClass('ui-icon-plus');
        button.addClass('ui-icon-minus');
      }
    });
    dt.prepend(minmax);
  });

  // Bind events
  var js_widget = this;
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
};

Faceted.DebugWidget.prototype = {
  synchronize: function(){
    var context = this;
    var query = jQuery.extend({}, Faceted.Query);
    query['debugger'] = this.wid;
    jQuery.get(Faceted.BASEURL + '@@faceted.widget.debug.query', query, function(data){
      if(data == "[]"){
        jQuery('.debug-query', context.widget).hide();
      }else{
        jQuery('dt.debug-query', context.widget).show();
      }
      context.query_area.text(data);
    });
    jQuery.get(Faceted.BASEURL + '@@faceted.widget.debug.after', query, function(data){
      if(data == "[]"){
        jQuery('.debug-after', context.widget).hide();
      }else{
        jQuery('dt.debug-after', context.widget).show();
      }
      context.after_area.text(data);
    });
    jQuery.get(Faceted.BASEURL + '@@faceted.widget.debug.criteria', query, function(data){
      if(data == "[]"){
        jQuery('.debug-config', context.widget).hide();
      }else{
        jQuery('dt.debug-config', context.widget).show();
      }
      context.config_area.text(data);
    });
    jQuery.get(Faceted.BASEURL + '@@faceted.widget.debug.counters', query, function(data){
      if(data == "[]"){
        jQuery('.debug-count', context.widget).hide();
      }else{
        jQuery('dt.debug-count', context.widget).show();
      }
      context.count_area.text(data);
    });
  },

  criteria: function(){
    return [];
  }
};

Faceted.initializeDebugWidget = function(evt){
  jQuery('div.faceted-debug-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.DebugWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeDebugWidget);
});
