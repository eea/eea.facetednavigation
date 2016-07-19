FacetedEdit.SelectWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.elements = jQuery('option', this.widget);
  this.select = jQuery('#' + this.wid);
  var value = this.select.val();

  // Handle change
  var js_widget = this;
  this.select.change(function(evt){
    js_widget.set_default(this);
  });

  this.count();
};

FacetedEdit.SelectWidget.prototype = {
  count: function(){
    if(!this.widget.hasClass('faceted-count')){
      return;
    }
    this.elements.each(function(){
      var option = jQuery(this);
      var number = Math.floor(Math.random() * 100);
      var option_txt = option.attr('title');
      option_txt += ' (' + number + ')';
      option.html(option_txt);
    });
  },

  set_default: function(element){
    var value = this.select.val();

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

FacetedEdit.initializeSelectWidget = function(){
  jQuery('div.faceted-select-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.SelectWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeSelectWidget);
});
