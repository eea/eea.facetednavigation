Faceted.ResultsPerPageWidget = function(wid) {
  this.wid = wid;
  this.widget = jQuery('#' + this.wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.elements = jQuery('option', this.widget);
  this.select = jQuery('#' + this.wid);
  this.selected = [];

  // Handle change
  jQuery('form', this.widget).submit(function() {
    return false;
  });

  var js_widget = this;
  this.select.change(function(evt) {
    js_widget.select_change(this, evt);
  });

  // Default value
  var value = this.select.val();
  if (value) {
    this.selected = jQuery('option[value=' + value + ']', this.widget);
    Faceted.Query[this.wid] = [ value ];
  }

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt) {
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt) {
    js_widget.reset();
  });
};

Faceted.ResultsPerPageWidget.prototype = {
  select_change : function(element, evt) {
    if (!jQuery(element).val()) {
      element = null;
    }
    this.do_query(element);
  },

  do_query : function(element) {
    if (!element) {
      this.selected = [];
      return Faceted.Form.do_query(this.wid, []);
    } else {
      var value = jQuery(element).val();
      this.selected = jQuery('#' + this.wid + '_widget option[value=' + value + ']');
      return Faceted.Form.do_query(this.wid, value);
    }
  },

  reset : function() {
    this.select.val("");
    this.selected = [];
  },

  synchronize : function() {
    var value = Faceted.Query[this.wid];
    if (!value) {
      this.reset();
      return;
    }

  var context = this;
  jQuery.each(value, function() {
    var selected = jQuery('#' + context.wid + '_widget option[value=' + value + ']');
    if (!selected.length) {
      context.reset();
    } else {
      context.selected = selected;
      context.select.val(value);
    }
  });
},

  criteria : function() {
    var html = [];
    var title = this.criteria_title();
    var body = this.criteria_body();
    if (title) {
      html.push(title);
    }
    if (body) {
      html.push(body);
    }
    return html;
  },

  criteria_title : function() {
    if (!this.selected.length) {
      return '';
    }

  var link = jQuery('<a href="#">[X]</a>');
  link.attr('id', 'criteria_' + this.wid);
  link.attr('title', 'Remove ' + this.title + ' filters');
  var widget = this;
  link.click(function(evt) {
    widget.criteria_remove();
    return false;
  });

  var html = jQuery('<dt>');
  html.attr('id', 'criteria_' + this.wid + '_label');
  html.append(link);
  html.append('<span>' + this.title + '</span>');
  return html;
},

  criteria_body : function() {
    if (!this.selected.length) {
      return '';
    }

  var widget = this;
  var html = jQuery('<dd>');
  var span = jQuery('<span class="faceted-resultsperpage-criterion">');
  html.attr('id', 'criteria_' + this.wid + '_entries');
  var element = jQuery(this.selected);
  var value = element.val();
  var label = element.html();
  var link = jQuery('<a href="#">[X]</a>');

  link.attr('id', 'criteria_' + this.wid + '_' + value);
  link.attr('title', 'Remove ' + label + ' filter');
  link.click(function(evt) {
    widget.criteria_remove();
    return false;
  });
  span.append(link);
  jQuery('<span>').text(label).appendTo(span);
  html.append(span);
  return html;
},

  criteria_remove : function() {
    this.select.val('');
    this.do_query();
  }
};

Faceted.initializeResultsPerPageWidget = function(evt) {
  jQuery('div.faceted-resultsperpage-widget').each(function() {
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.ResultsPerPageWidget(wid);
  });
};

jQuery(document).ready(
  function() {
    jQuery(Faceted.Events).bind(Faceted.Events.INITIALIZE,
      Faceted.initializeResultsPerPageWidget);
  });
