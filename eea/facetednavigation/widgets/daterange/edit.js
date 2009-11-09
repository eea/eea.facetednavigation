FacetedEdit.DateRangeWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.years = jQuery('select[name=' + wid + '_year]', this.widget);
  this.months = jQuery('select[name=' + wid + '_month]', this.widget);
  this.days = jQuery('select[name=' + wid + '_day]', this.widget);
  this.start = jQuery('input[name=' + wid + ']', this.widget)[0];
  this.end = jQuery('input[name=' + wid + ']', this.widget)[1];
  this.selected = [this.start, this.end];

  var js_widget = this;
  this.years.change(function(evt){
    js_widget.set_default(this);
  });

  this.months.change(function(evt){
    js_widget.set_default(this);
  });

  this.days.change(function(evt){
    js_widget.set_default(this);
  });

};

FacetedEdit.DateRangeWidget.prototype = {
  set_default: function(element){
    if(jQuery(this.years[0]).val()=='0000' || jQuery(this.years[1]).val() == '0000'){
      return;
    }
    if(jQuery(this.months[0]).val()=='00' || jQuery(this.months[1]).val() == '00'){
      return;
    }
    if(jQuery(this.days[0]).val()=='00' || jQuery(this.days[1]).val()=='00'){
      return;
    }
    var start = jQuery(this.start).val();
    var end = jQuery(this.end).val();
    start = new Date(start.replace(/-/g, '/'));
    end = new Date(end.replace(/-/g, '/'));
    if(end<start){
      var msg = 'End Date should be greater than Start date';
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: msg});
      return;
    }

    var start_str = start.getFullYear() + '/' + (start.getMonth() + 1) + '/' + start.getDate();
    var end_str = end.getFullYear() + '/' + (end.getMonth() + 1) + '/' + end.getDate();
    var value = start_str + '=>' + end_str;
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

FacetedEdit.initializeDateRangeWidget = function(){
  jQuery('div.faceted-daterange-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.DateRangeWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeDateRangeWidget);
});
