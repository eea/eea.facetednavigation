FacetedEdit.PathWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  var tree = new FacetedTree.JsTree(this.wid, this.widget, 'edit');

  var js_widget = this;
  jQuery(FacetedTree.Events).bind(FacetedTree.Events.AJAX_STOP, function(evt, data){
    js_widget.initialize(data.msg);
    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: 'Done'});
  });
};

FacetedEdit.PathWidget.prototype = {
  initialize: function(data){
    if(!data.length){
      return;
    }

    this.form = jQuery('form', this.widget);
    this.input = jQuery('input', this.widget);
    this.selected = this.input;

    var js_widget = this;
    this.form.submit(function(evt){
      js_widget.set_default(js_widget.input);
      return false;
    });

    // Navigation Tree

  jQuery(FacetedTree.Events).bind(FacetedTree.Events.CHANGED, function(data){
    js_widget.set_default(js_widget.input);
  });

  },

  set_default: function(element){
    this.selected = this.input;
    var value = this.selected.val();

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
