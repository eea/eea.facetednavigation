/* Relative Date Widget
*/
Faceted.DateWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.operation = jQuery('#' + this.wid + '_operation', this.widget);
  this.value = jQuery('#' + this.wid + '_value', this.widget);
  this.daterange = jQuery('#' + this.wid + '_daterange', this.widget);
  this.selected = [];

  // Default value
  var operation = this.operation.val();
  var daterange = this.daterange.val();
  var value = this.value.val();

  if(operation !== '' && daterange !== '' && value !== ''){
    this.selected = [this.operation, this.value, this.daterange];
    Faceted.Query[this.wid] = [operation, value, daterange];
  }

  // Handle clicks
  jQuery('form', this.widget).submit(function(){
    return false;
  });

  var js_widget = this;
  this.operation.change(function(evt){
    js_widget.select_change(this, evt);
  });

  this.value.change(function(evt){
    js_widget.select_change(this, evt);
  });

  this.daterange.change(function(evt){
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

Faceted.DateWidget.prototype = {
  select_change: function(element, evt){
    if(!jQuery(element).val()){
      this.reset();
      Faceted.Form.do_query(this.wid, []);
      return;
    }
    if(this.value.val() == '0' && this.operation.val()){
      if(this.operation.val() == 'more'){
        this.daterange.val('future');
      }else{
        this.daterange.val('past');
      }
      this.do_query(element);
    }else if(this.operation.val() && this.value.val() && this.daterange.val()){
      this.do_query(element);
    }
  },

  do_query: function(element){
      var value = [this.operation.val(), this.value.val(), this.daterange.val()];
      this.selected = [this.operation, this.value, this.daterange];
      Faceted.Form.do_query(this.wid, value);
  },

  reset: function(){
    this.selected = [];
    this.operation.val('');
    this.value.val('');
    this.daterange.val('');
  },

  synchronize: function(){
    var q_value = Faceted.Query[this.wid];
    if(!q_value){
      this.reset();
      return;
    }
    if(!q_value.length){
      this.reset();
      return;
    }
    if(q_value.length<3){
      this.reset();
      return;
    }

    this.operation.val(q_value[0]);
    this.value.val(q_value[1]);
    this.daterange.val(q_value[2]);
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

    var operation = this.operation.val();
    var value = this.value.val();
    value = parseInt(value, 10);
    var daterange = this.daterange.val();
    var start = new Date('01/01/1970');
    var end = new Date('12/31/2030');
    var now = new Date();
    var day = 24 * 3600 * 1000;

    if(operation == 'less'){
      if(value === 0){
        end = new Date();
      }else{
        if(daterange == 'past'){
          start = new Date(now.getTime() - value * day);
          end = new Date();
        }else{
          start = new Date();
          end = new Date(now.getTime() + value * day);
        }
      }
    }
    else if(operation == 'more'){
      if(value === 0){
        start = new Date();
      }else{
        if(daterange == 'past'){
          end = new Date(now.getTime() - value * day);
        }else{
          start = new Date(now.getTime() + value * day);
        }
      }
    }
    else if(operation == 'equal'){
      if(value === 0){
        start = new Date();
        end = new Date();
      }else{
        if(daterange == 'past'){
          start = new Date(now.getTime() - value * day);
          end = new Date(now.getTime() - value * day);
        }else{
          start = new Date(now.getTime() + value * day);
          end = new Date(now.getTime() + value * day);
        }
      }
    }

    var widget = this;
    var html = jQuery('<dd>');
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
    this.operation.val('');
    this.daterange.val('');
    this.value.val('');
    return Faceted.Form.do_query(this.wid, []);
  }
};

Faceted.initializeDateWidget = function(evt){
  jQuery('div.faceted-date-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.DateWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeDateWidget);
});
