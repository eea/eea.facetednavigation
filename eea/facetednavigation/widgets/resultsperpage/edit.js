FacetedEdit.ResultsPerPageWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.elements = jQuery('option', this.widget);
  this.select = jQuery('#' + this.wid);
  var value = this.select.val();
  this.selected = jQuery('option[value='+ value +']', this.widget);

  // Handle change
  var js_widget = this;
  this.select.change(function(evt){
    js_widget.set_default(this);
  });
};

FacetedEdit.ResultsPerPageWidget.prototype = {
  set_default: function(element){
    var value = this.select.val();
    this.selected = jQuery('option[value='+ value +']', this.widget);

    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query[this.wid + '_default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeResultsPerPageWidget = function(){
  jQuery('div.faceted-resultsperpage-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.ResultsPerPageWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeResultsPerPageWidget);
});
