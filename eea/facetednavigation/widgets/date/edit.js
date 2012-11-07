FacetedEdit.DateWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.select_from = jQuery('select[name=from]', this.widget);
  this.select_to = jQuery('select[name=to]', this.widget);

  this.select_from.hide();
  this.select_to.hide();

  var js_widget = this;
  jQuery('select', this.widget).selectToUISlider({
    labels: 2,
    labelSrc: 'text',
    sliderOptions: {
      change: function(){
        js_widget.set_default(js_widget.select_from, js_widget.select_to);
      }
    }
  });

  jQuery('span.ui-slider-label', this.widget).each(function(index){
    if(index!==11){
      return;
    }
    var span = jQuery(this);
    span.addClass('ui-slider-label-show');
  });

  this.selected = [];
};

FacetedEdit.DateWidget.prototype = {
  set_default: function(from, to){
    var from_val = from.val();
    var to_val = to.val();
    var value = '';
    if((from_val === 'now-past') && (to_val === 'now_future')){
      value = '';
    }else{
      value = from_val + '=>' + to_val;
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

FacetedEdit.initializeDateWidget = function(){
  jQuery('div.faceted-date-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.DateWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeDateWidget);
});
