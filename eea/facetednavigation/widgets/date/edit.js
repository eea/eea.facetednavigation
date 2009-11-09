FacetedEdit.DateWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.operation = jQuery('#' + this.wid + '_operation', this.widget);
  this.value = jQuery('#' + this.wid + '_value', this.widget);
  this.daterange = jQuery('#' + this.wid + '_daterange', this.widget);

  var js_widget = this;
  this.operation.change(function(evt){
    js_widget.set_default(this);
  });

  this.value.change(function(evt){
    js_widget.set_default(this);
  });

  this.daterange.change(function(evt){
    js_widget.set_default(this);
  });
};

FacetedEdit.DateWidget.prototype = {
  set_default: function(element){
    if(!jQuery(element).val()){
      this.reset_default(element);
      return;
    }

    var res = '';
    var operation = this.operation.val();
    var value = this.value.val();
    var daterange = this.daterange.val();

    if(operation == 'more' || operation == 'less'){
      operation += ' than';
    }
    res += operation + ' ';

    if(value == '0'){
      value = 'now';
    }
    else if(value == '1'){
      value += ' day';
    }else{
      value += ' days';
    }
    res += value;

    if(daterange == 'past'){
      daterange = ' in the past';
    }else{
      daterange = ' in the future';
    }
    res += daterange;

    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query[this.wid + '_default'] = res;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post('@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  },

  reset_default: function(element){

    this.operation.val('');
    this.value.val('');
    this.daterange.val('');

    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query[this.wid + '_default'] = '';

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post('@@faceted_configure', query, function(data){
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
