FacetedEdit.SortingWidget = function(wid, context){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.reverse = jQuery('#' + this.wid + '_reversed');
  this.elements = jQuery('option', this.widget);
  this.select = jQuery('#' + this.wid);

  var value = this.select.val();
  this.selected = jQuery('option[value=' + value + ']', this.widget);

  // Handle select change
  var js_widget = this;
  this.select.change(function(evt){
    js_widget.set_default(this);
  });
  this.reverse.click(function(evt){
    js_widget.set_default(this);
  });

};

FacetedEdit.SortingWidget.prototype = {
  set_default: function(element){
    var value = this.select.val();
    this.selected = jQuery('option[value=' + value + ']', this.widget);
    if(this.reverse.attr('checked')){
      value += '(reverse)';
    }

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

FacetedEdit.initializeSortingWidget = function(){
  jQuery('div.faceted-sorting-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.SortingWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeSortingWidget);
});
