/* Path Widget
*/
Faceted.PathWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.input = jQuery('input', this.widget);
  this.breadcrumbs = jQuery('<dd>');
  this.selected = [];

  // Default value
  var value = this.input.val();
  if(value){
    this.selected = this.input;
    Faceted.Query[this.wid] = [value];
  }

  // Navigation Tree
  var tree = new FacetedTree.JsTree(this.wid, this.widget);

  // Bind events
  var js_widget = this;
  jQuery('form', this.widget).submit(function(){
    return false;
  });
  jQuery(FacetedTree.Events).bind(FacetedTree.Events.CHANGED, function(data){
    js_widget.text_change(js_widget.input);
  });
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
    html.attr('id', 'criteria_' + this.wid + '_label');
    html.append(link);
    html.append('<span>' + this.title + '</span>');
    return html;
  },

  criteria_body: function(){
    if(!this.selected.length){
      return '';
    }

    var js_widget = this;
    js_widget.breadcrumbs.text('Loading...');
    var query = {};
    query.path = js_widget.input.val();
    query.cid = js_widget.wid;
    jQuery.getJSON(Faceted.BASEURL + '@@faceted.path.breadcrumbs.json', query, function(data){
      js_widget.breadcrumbs.empty();
      jQuery.each(data, function(){
        js_widget.breadcrumbs.append(jQuery('<span>').html('&raquo;'));
        var a = jQuery('<a>');
        a.attr('href', this.url);
        a.attr('title', this.title);
        a.text(this.title);
        a.click(function(){
          var path = jQuery(this).attr('href');
          js_widget.input.val(path);
          jQuery(FacetedTree.Events).trigger(
            FacetedTree.Events.CHANGED, {path: path}
          );
          return false;
        });
        js_widget.breadcrumbs.append(a);
      });
    });
    return js_widget.breadcrumbs;
  },

  criteria_remove: function(){
    this.selected = [];
    this.input.val('');
    this.do_query();
  }
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
