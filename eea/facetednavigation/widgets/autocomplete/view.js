/* Autocomplete Widget
*/
Faceted.AutocompleteWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.selected = [];
  this.button = jQuery('input[type=submit]', this.widget);

  // Handle text change
  var js_widget = this;
  jQuery('form', this.widget).submit(function(){
    js_widget.text_change(js_widget.button);
    return false;
  });

  // Default value
  var input = jQuery('#' + this.wid);
  var value = input.val();
  if(value){
    this.selected = input;
    Faceted.Query[this.wid] = [value];
  }

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
};

Faceted.AutocompleteWidget.prototype = {
  text_change: function(element, evt){
    this.do_query(element);
    jQuery(element).removeClass("submitting");
  },

  do_query: function(element){
    var input = jQuery('#' + this.wid);
    var value = input.val();
    value = value ? [value] : [];

    if(!element){
      this.selected = [];
      return Faceted.Form.do_query(this.wid, []);
    }
    this.selected = [input];

    var where = jQuery('input[type=radio]:checked', this.widget);
    where = where.length == 1 ? where.val() : 'all';
    if(where == 'all'){
      return Faceted.Form.do_query(this.wid, value);
    }

    var current = Faceted.Query[this.wid];
    current = current ? current : [];
    if(value.length && !(value[0] in current)){
      current.push(value[0]);
    }
    return Faceted.Form.do_query(this.wid, current);
  },

  reset: function(){
    this.selected = [];
    jQuery('#' + this.wid).val('');
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
      return;
    }

    var input = jQuery('#value_' + this.wid);
    input.attr('value', value);
    this.selected = [input];
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
    var elements = Faceted.Query[this.wid];
    elements = elements ? elements: [];
    jQuery.each(elements, function(){
      var label = this.toString();
      if(label.length>0){
          var span = jQuery('<span class="faceted-autocomplete-criterion">');
          var link = jQuery('<a href="#">[X]</a>');
          link.attr('id', 'criteria_' + widget.wid + '_' + label);
          link.attr('title', 'Remove ' + label + ' filter');
          link.click(function(evt){
            widget.criteria_remove(label);
            return false;
          });
          span.append(link);
          jQuery('<span>').text(label).appendTo(span);
          html.append(span);
      }
    });
    return html;
  },

  criteria_remove: function(value){
    jQuery('#' + this.wid).val('');
    if(!value){
      this.selected = [];
      this.do_query();
      return;
    }
    jQuery('#' + this.wid + '_place_current', this.widget).attr('checked', true);
    var element = jQuery('input[type=text]', this.widget);
    var current = Faceted.Query[this.wid];
    var index = jQuery.inArray(value, current);
    if(index == -1){
      return;
    }
    current.splice(index, 1);
    Faceted.Query[this.wid] = current;
    this.do_query(element);
  }
};

Faceted.initializeAutocompleteWidget = function(evt){
  jQuery('div.faceted-autocomplete-widget').each(function(){
    var wid = jQuery(this).attr('id');
    var autocomplete_view = jQuery(this).attr('data-autocomplete-view');
    var multiple = (jQuery(this).attr('data-multiple') === 'true');
    var placeholder = jQuery(this).attr('data-placeholder');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.AutocompleteWidget(wid);

    jQuery("#" + wid).select2({
      placeholder: placeholder,
      multiple: multiple,
      allowClear: true,
      minimumInputLength: 2,
      ajax: {
        url: autocomplete_view,
        delay: 250,
        dataType: 'json',
        data: function (term, page) {
            return {
                term: term,
                add_terms: true
            };
        },
        results: function (data, page) {
            return {
                results: data
            };
        },
        cache: false
      }
    });
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeAutocompleteWidget);
});
