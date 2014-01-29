/* Relative Date Widget
*/
Faceted.DateWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.select_from = jQuery('select[name=from]', this.widget);
  this.select_to = jQuery('select[name=to]', this.widget);

  this.select_from.hide();
  this.select_to.hide();

  var js_widget = this;
  this.slider = jQuery('select', this.widget).selectToUISlider({
    labels: 2,
    labelSrc: 'text',
    sliderOptions: {
      change: function(){
        js_widget.change();
      }
    }
  });

  jQuery('span.ui-slider-label', this.widget).each(function(i){
    if(i!==11){
      return;
    }
    var span = jQuery(this);
    span.addClass('ui-slider-label-show');
  });

  this.selected = [];

  // Default value
  var from = this.select_from.val();
  var to = this.select_to.val();
  if((from !== 'now-past') || (to !== 'now_future')){
    this.selected = [this.select_from, this.select_to];
    Faceted.Query[this.wid] = [from, to];
  }

  // Handle clicks
  jQuery('form', this.widget).submit(function(){
    return false;
  });

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset_ui();
  });
};

Faceted.DateWidget.prototype = {
  change: function(){
    var from = this.select_from.val();
    var to = this.select_to.val();
    if(from === 'now-past' && to === 'now_future'){
      this.reset();
      Faceted.Form.do_query(this.wid, []);
    }else{
      this.do_query();
    }
  },

  do_query: function(){
    var value = [this.select_from.val(), this.select_to.val()];
    this.selected = [this.select_from, this.select_to];
    Faceted.Form.do_query(this.wid, value);
  },

  reset: function(){
    this.selected = [];
    this.select_from.val('now-past');
    this.select_to.val('now_future');
  },

  reset_ui: function(){
    this.reset();
    this.select_from.trigger('change');
    this.select_to.trigger('change');
  },

  synchronize: function(){
    var q_value = Faceted.Query[this.wid];
    if(!q_value){
      this.reset_ui();
      return;
    }
    if(!q_value.length){
      this.reset_ui();
      return;
    }
    if(q_value.length<2){
      this.reset_ui();
      return;
    }

    this.select_from.val(q_value[0]).trigger('change');
    this.select_to.val(q_value[1]).trigger('change');
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

    var from = jQuery('option:selected', this.select_from).text();
    var to = jQuery('option:selected', this.select_to).text();
    var label = from + ' - ' + to;

    var widget = this;
    var html = jQuery('<dd>');
    html.attr('id', 'criteria_' + this.wid + '_entries');
    var span = jQuery('<span class="faceted-date-criterion">');
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
    this.reset_ui();
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
