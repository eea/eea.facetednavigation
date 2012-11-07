FacetedEdit.DebugWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
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

  var js_widget = this;
  jQuery(FacetedEdit.Events).bind(FacetedEdit.Events.AJAX_STOP, function(evt, data){
    js_widget.update(data);
  });
};

FacetedEdit.DebugWidget.prototype = {
  update: function(){
    var context = this;
    var query = {};
    query['debugger'] = this.wid;
    query.mode = 'edit';
    jQuery.get(FacetedEdit.BASEURL + '@@faceted.widget.debug.query', query, function(data){
      if(data == "[]"){
        jQuery('.debug-query', context.widget).hide();
      }else{
        jQuery('dt.debug-query', context.widget).show();
      }
      context.query_area.text(data);
    });
    jQuery.get(FacetedEdit.BASEURL + '@@faceted.widget.debug.after', query, function(data){
      if(data == "[]"){
        jQuery('.debug-after', context.widget).hide();
      }else{
        jQuery('dt.debug-after', context.widget).show();
      }
      context.after_area.text(data);
    });
    jQuery.get(FacetedEdit.BASEURL + '@@faceted.widget.debug.criteria', query, function(data){
      if(data == "[]"){
        jQuery('.debug-config', context.widget).hide();
      }else{
        jQuery('dt.debug-config', context.widget).show();
      }
      context.config_area.text(data);
    });
    jQuery.get(FacetedEdit.BASEURL + '@@faceted.widget.debug.counters', query, function(data){
      if(data == "[]"){
        jQuery('.debug-count', context.widget).hide();
      }else{
        jQuery('dt.debug-count', context.widget).show();
      }
      context.count_area.text(data);
    });
  }
};

FacetedEdit.initializeDebugWidget = function(){
  jQuery('div.faceted-debug-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.DebugWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeDebugWidget);
});
