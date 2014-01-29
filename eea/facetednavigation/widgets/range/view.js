/* Range Widget
*/

Faceted.RangeWidget = function(wid){
  var js_widget = this;
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();

  this.start = jQuery('input[name=start]', this.widget);
  this.end = jQuery('input[name=end]', this.widget);
  this.selected = [];

  var start = this.start.val();
  var end = this.end.val();
  if(start && end){
    this.selected = [this.start, this.end];
    Faceted.Query[this.wid] = [start, end];
  }

  // Handle clicks
  jQuery('form', this.widget).submit(function(){
    return false;
  });
  var handle = function(evt){js_widget.select_change(this, evt);};
  this.start.change(handle);
  this.end.change(handle);

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
};

Faceted.RangeWidget.prototype = {
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
    if(end<start){
      var msg = 'Invalid range';
      Faceted.Form.raise_error(msg, this.wid + '_errors', []);
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
    var span = jQuery('<span class="faceted-range-criterion">');
    var start = this.start.val();
    var end = this.end.val();

    var label = start + ' - ' + end;
    var link = jQuery('<a href="#">[X]</a>');

    link.attr('id', 'criteria_' + this.wid + '_');
    link.attr('title', 'Remove ' + label + ' filter');
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });
    span.append(link);
    jQuery('<span>').text(label).appendTo(span);
    html.append(span);
    return html;
  },

  criteria_remove: function(){
    this.reset();
    return Faceted.Form.do_query(this.wid, []);
  }
};

Faceted.initializeRangeWidget = function(evt){
  jQuery('div.faceted-range-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.RangeWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeRangeWidget);
});
