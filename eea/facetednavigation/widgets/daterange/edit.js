FacetedEdit.DateRangeWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');

  this.yearRange =  jQuery('input[name=calYearRange]', this.widget).val();
  this.start = jQuery('input[name=start]', this.widget);
  this.end = jQuery('input[name=end]', this.widget);

  var js_widget = this;
  this.start.datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'yy-mm-dd',
    yearRange: this.yearRange,
    onSelect: function(date, cal){
      js_widget.set_default(date);
    }
  });

  this.end.datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'yy-mm-dd',
    yearRange: this.yearRange,
    onSelect: function(date, cal){
      js_widget.set_default(date);
    }
  });

  this.start.change(function(){
    js_widget.set_default(this);
  });

  this.end.change(function(){
    js_widget.set_default(this);
  });
};

FacetedEdit.DateRangeWidget.prototype = {
  set_default: function(element){
    var start = this.start.val();
    var end = this.end.val();
    if((!start && end) || (start && !end)){
      return;
    }

    var value = '';
    if(start && end){
      var start_date = new Date(start.replace(/-/g, '/'));
      var end_date = new Date(end.replace(/-/g, '/'));
      if(end_date<start_date){
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
    query[this.wid + '_default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
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
