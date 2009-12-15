/* Path Widget
*/
Faceted.PathWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.input = jQuery('input', this.widget);
  this.selected = [];

  // Handle text change
  var js_widget = this;
  jQuery('form', this.widget).submit(function(){
    js_widget.text_change(js_widget.input);
    return false;
  });

  // Default value
  var value = this.input.val();
  if(value){
    this.selected = this.input;
    Faceted.Query[this.wid] = [value];
  }

  // Navigation Tree
  var tree = new FacetedTree.JsTree(this.wid, this.widget);

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
};

Faceted.PathWidget.prototype = {
  text_change: function(element, evt){
    this.do_query(element);
  },

  do_query: function(element){
    var value = this.input.val();
    value = value ? [value] : [];

    if(!element){
      this.selected = [];
      return Faceted.Form.do_query(this.wid, []);
    }
    this.selected = [this.input];
    return Faceted.Form.do_query(this.wid, value);
  },

  reset: function(){
    this.selected = [];
    this.input.val('');
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
      return;
    }
    this.selected = [this.input];
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
    var id = widget.input.attr('id');
    var title = widget.input.val();
    var link = jQuery('<a href="#">[X]</a>');

    link.attr('id', 'criteria_' + id);
    link.attr('title', 'Remove ' + title + ' filter');
    link.click(function(evt){
      widget.criteria_remove();
      return false;
    });
    html.append(link);
    html.append('<span>' + title + '</span>');

    return html;
  },

  criteria_remove: function(){
    this.selected = [];
    this.input.val('');
    this.do_query();
  },
};

Faceted.initializePathWidget = function(evt){
  jQuery('div.faceted-path-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.PathWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializePathWidget);
});
