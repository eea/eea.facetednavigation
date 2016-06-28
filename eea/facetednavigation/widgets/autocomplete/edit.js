FacetedEdit.AutocompleteWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.button = jQuery('input[type=submit]', this.widget);
  this.input = jQuery('#' + this.wid);
  this.selected = this.input;

  var js_widget = this;
  this.button.click(function(evt){
    js_widget.set_default(this);
  });

  this.input.change(function(evt){
    js_widget.set_default(this);
  });
};

FacetedEdit.AutocompleteWidget.prototype = {
  set_default: function(element){
    this.selected = this.input;
    var value = this.selected.val();

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

FacetedEdit.initializeAutocompleteWidget = function(){
  jQuery('div.faceted-autocomplete-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.AutocompleteWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeAutocompleteWidget);
});
