/* DateRange Widget
*/
Faceted.DateRangeWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.hours = jQuery('input[name=' + wid + '_hour]');
  this.mins = jQuery('input[name=' + wid + '_minute]');
  this.years = jQuery('select[name=' + wid + '_year]');
  this.months = jQuery('select[name=' + wid + '_month]');
  this.days = jQuery('select[name=' + wid + '_day]');
  this.start = jQuery('input[name=' + wid + ']')[0];
  this.end = jQuery('input[name=' + wid + ']')[1];
  this.selected = [];

  this.initialize();
  // Handle clicks
  jQuery('form', this.widget).submit(function(){
    return false;
  });

  var js_widget = this;
  this.years.change(function(evt){
    js_widget.select_change(this, evt);
  });

  this.months.change(function(evt){
    js_widget.select_change(this, evt);
  });

  this.days.change(function(evt){
    js_widget.select_change(this, evt);
  });

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
};

Faceted.DateRangeWidget.prototype = {
  initialize: function(){
    jQuery(this.hours[0]).val('00');
    jQuery(this.mins[0]).val('00');
    jQuery(this.hours[1]).val('23');
    jQuery(this.mins[1]).val('59');

    // Default value
    var start = jQuery(this.start).val();
    if(!start){
      return;
    }
    var end = jQuery(this.end).val();
    if(!end){
      return;
    }

    if(start.search(':')==-1){
      start = start + ' 00:00';
    }
    if(end.search(':')==-1){
      end = end + ' 23:59';
    }

    Faceted.Query[this.wid] = [start, end];
    this.synchronize();
  },

  select_change: function(element, evt){
    this.do_query(element);
  },

  do_query: function(element){
    if(jQuery(this.years[0]).val()=='0000' || jQuery(this.years[1]).val() == '0000'){
      this.selected = [];
      return;
    }
    if(jQuery(this.months[0]).val()=='00' || jQuery(this.months[1]).val() == '00'){
      this.selected = [];
      return;
    }
    if(jQuery(this.days[0]).val()=='00' || jQuery(this.days[1]).val()=='00'){
      this.selected = [];
      return;
    }

    var start = jQuery(this.start).val();
    var end = jQuery(this.end).val();
    if(start.search(':')==-1){
      start = start + ' 00:00';
    }
    if(end.search(':')==-1){
      end = end + ' 23:59';
    }
    var value = [start, end];
    start = new Date(start.replace(/-/g, '/'));
    end = new Date(end.replace(/-/g, '/'));

    if(end<=start){
      var msg = 'End Date should be greater than Start date';
      Faceted.Form.raise_error(msg, this.wid+'_errors', [this.wid+'_end']);
    }else{
      this.selected = [this.start, this.end];
      Faceted.Form.clear_errors(this.wid+'_errors', [this.wid+'_end']);
      Faceted.Form.do_query(this.wid, value);
    }
  },

  reset: function(){
    this.selected = [];
    this.years.val('0000');
    this.months.val('00');
    this.days.val('00');
    jQuery(this.start).val('');
    jQuery(this.end).val('');
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
      return;
    }
    if(!value.length){
      this.reset();
      return;
    }
    if(value.length<2){
      this.reset();
      return;
    }

    var start = value[0];
    var end = value[1];
    var start_date = new Date(start.replace(/-/g, '/'));
    var end_date = new Date(end.replace(/-/g, '/'));
    // Invalid date
    if(!start_date.getFullYear()){
      this.reset();
      return;
    }
    if(!end_date.getFullYear()){
      this.reset();
      return;
    }

    var context = this;
    // Set start, end inputs
    jQuery(this.start).val(start);
    jQuery(this.end).val(end);
    this.selected = [this.start, this.end];

    jQuery.each([start_date, end_date], function(index){
      // Set years
      jQuery(context.years[index]).val(this.getFullYear());
      // Set months
      var month = this.getMonth();
      month += 1;
      if(month<10){
        month = '0' + month;
      }
      jQuery(context.months[index]).val(month);
      // Set days
      jQuery(context.days[index]).val(this.getDate());
    });
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
    var start = jQuery(this.start).val();
    var end = jQuery(this.end).val();
    start = new Date(start.replace(/-/g, '/'));
    end = new Date(end.replace(/-/g, '/'));

    var label = start.toDateString() + ' - ' + end.toDateString();
    var link = jQuery('<a href="#">[X]</a>');

    link.attr('id', 'criteria_' + this.wid + '_');
    link.attr('title', 'Remove ' + label + ' filter');
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });
    html.append(link);
    html.append('<span>' + label + '</span>');

    return html;
  },

  criteria_remove: function(){
    this.selected = [];
    this.years.val('0000');
    this.months.val('00');
    this.days.val('00');
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
