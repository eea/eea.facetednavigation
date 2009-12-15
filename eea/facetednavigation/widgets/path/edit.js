FacetedEdit.PathWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.form = jQuery('form', this.widget);
  this.input = jQuery('input', this.widget);
  this.selected = this.input;

  var js_widget = this;
  this.form.submit(function(evt){
    js_widget.set_default(js_widget.input);
    return false;
  });

  // Navigation Tree
  var tree = new FacetedTree.JsTree(this.wid, this.widget);
  jQuery(FacetedTree.Events).bind(FacetedTree.Events.CHANGED, function(data){
    js_widget.set_default(js_widget.input);
  });
};

FacetedEdit.PathWidget.prototype = {
  set_default: function(element){
    this.selected = this.input;
    var value = this.selected.val();

    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query[this.wid + '_default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post('@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializePathWidget = function(){
  jQuery('div.faceted-path-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.PathWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializePathWidget);
});
