FacetedEdit.RangeWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.start = jQuery('input[name=start]', this.widget);
  this.end = jQuery('input[name=end]', this.widget);

  var js_widget = this;
  this.start.change(function(){
    js_widget.set_default(this);
  });

  this.end.change(function(){
    js_widget.set_default(this);
  });
};

FacetedEdit.RangeWidget.prototype = {
  set_default: function(element){
    var start = this.start.val();
    var end = this.end.val();
    if((!start && end) || (start && !end)){
      return;
    }

    var value = '';
    if(start && end){
      if(end<start){
        var msg = 'End Date should be greater than Start date';
        jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: msg});
        return;
      }
      value = start + '=>' + end;
    }
    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query['faceted.' + this.wid + '.default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeRangeWidget = function(){
  jQuery('div.faceted-range-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.RangeWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeRangeWidget);
});
