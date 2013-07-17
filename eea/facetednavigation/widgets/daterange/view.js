/* DateRange Widget
*/
Faceted.DateRangeWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();

  this.start = jQuery('input[name=start]', this.widget);
  this.yearRange =  jQuery('input[name=calYearRange]', this.widget).val();
  this.end = jQuery('input[name=end]', this.widget);
  this.selected = [];

  var start = this.start.val();
  var end = this.end.val();
  if(start && end){
    this.selected = [this.start, this.end];
    Faceted.Query[this.wid] = [start, end];
  }

  var js_widget = this;
  this.start.datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'yy-mm-dd',
    yearRange: this.yearRange,
    onSelect: function(date, cal){
      js_widget.select_change(js_widget.start);
    }
  });

  this.end.datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: this.yearRange,
    dateFormat: 'yy-mm-dd',
    onSelect: function(date, cal){
      js_widget.select_change(js_widget.end);
    }
  });

  // Handle clicks
  jQuery('form', this.widget).submit(function(){
    return false;
  });

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
};
Faceted.DateRangeErrorMsg = 'Invalid date range';
Faceted.DateRangeWidget.prototype = {
  select_change: function(element){
    this.do_query(element);
  },

  do_query: function(element){
    var start = this.start.val();
    var end = this.end.val();
    if(!start || !end){
      this.selected = [];
      return false;
    }

    var value = [start, end];
    var start_date = new Date(start.replace(/-/g, '/'));
    var end_date = new Date(end.replace(/-/g, '/'));

    if(end_date<start_date){
      Faceted.Form.raise_error(Faceted.DateRangeErrorMsg,
                               this.wid + '_errors', []);
    }else{
      this.selected = [this.start, this.end];
      Faceted.Form.clear_errors(this.wid + '_errors', []);
      Faceted.Form.do_query(this.wid, value);
    }
  },

  reset: function(){
    this.selected = [];
    this.start.val('');
    this.end.val('');
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
      return false;
    }
    if(!value.length){
      this.reset();
      return false;
    }
    if(value.length<2){
      this.reset();
      return false;
    }

    var start = value[0];
    var end = value[1];
    var start_date = new Date(start.replace(/-/g, '/'));
    var end_date = new Date(end.replace(/-/g, '/'));

    // Invalid date
    if(!start_date.getFullYear()){
      this.reset();
      return false;
    }
    if(!end_date.getFullYear()){
      this.reset();
      return false;
    }

    // Set start, end inputs
    this.start.val(start);
    this.end.val(end);
    this.selected = [this.start, this.end];
  },

  criteria: function(){
    var html = [];
    var title = this.criteria_title();
    var body = this.criteria_body();
    if(title){
      html.push(title);
    }
    if(body){
      html.push(body);
    }
    return html;
  },

  criteria_title: function(){
    if(!this.selected.length){
      return '';
    }

    var link = jQuery('<a href="#">[X]</a>');
    link.attr('id', 'criteria_' + this.wid);
    link.attr('title', 'Remove ' + this.title + ' filters');
    var widget = this;
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });

    var html = jQuery('<dt>');
    html.attr('id', 'criteria_' + this.wid + '_label');
    html.append(link);
    html.append('<span>' + this.title + '</span>');
    return html;
  },

  criteria_body: function(){
    if(!this.selected.length){
      return '';
    }

    var widget = this;
    var html = jQuery('<dd>');
    html.attr('id', 'criteria_' + this.wid + '_entries');
    var start = this.start.val();
    var end = this.end.val();
    var start_date = new Date(start.replace(/-/g, '/'));
    var end_date = new Date(end.replace(/-/g, '/'));

    var label = this.criteria_label(start_date, end_date);
    var link = jQuery('<a href="#">[X]</a>');

    link.attr('id', 'criteria_' + this.wid + '_');
    link.attr('title', 'Remove ' + label + ' filter');
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });
    var span = jQuery('<span class="faceted-daterange-criterion">');
    span.append(link);
    span.append('<span>' + label + '</span>');
    html.append(span);
    return html;
  },

  criteria_label: function(start_date, end_date){
    return start_date.toDateString() + ' - ' + end_date.toDateString();
  },

  criteria_remove: function(){
    this.reset();
    return Faceted.Form.do_query(this.wid, []);
  }
};

Faceted.initializeDateRangeWidget = function(evt){
  jQuery('div.faceted-daterange-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.DateRangeWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeDateRangeWidget);
});
