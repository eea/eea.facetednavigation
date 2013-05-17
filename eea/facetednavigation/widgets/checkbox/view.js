/* Checkboxes Widget
*/
Faceted.CheckboxesWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.fieldset = jQuery('.widget-fieldset', this.widget);
  this.title = jQuery('legend', this.widget).html();
  this.elements = jQuery('input[type=checkbox]', this.widget);
  this.maxitems = parseInt(jQuery('span', this.widget).text(), 10);
  this.operator = this.widget.attr('data-operator');
  this.selected = [];

  // Faceted version
  this.version = '';
  var version = jQuery('#faceted-version');
  if(version){
    this.version = version.text();
  }

  jQuery('form', this.widget).submit(function(){
    return false;
  });

  // Handle checkbox click
  var js_widget = this;
  this.elements.click(function(evt){
    js_widget.checkbox_click(this, evt);
  });

  // Default values
  var selected = jQuery('input[type=checkbox]:checked', this.widget);
  if(selected.length){
    this.selected = selected;
    Faceted.Query[this.wid] = [];
    selected.each(function(){
      Faceted.Query[js_widget.wid].push(jQuery(this).val());
    });
  }

  // Handle More/Less buttons click
  if(this.maxitems){
    this.fieldset.collapsible({
      maxitems: this.maxitems,
      elements: 'li:not(.faceted-checkbox-item-zerocount)'
    });
  }

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });
  if(this.widget.hasClass('faceted-count')){
    var sortcountable = this.widget.hasClass('faceted-sortcountable');
    jQuery(Faceted.Events).bind(Faceted.Events.QUERY_INITIALIZED, function(evt){
      js_widget.count(sortcountable);
    });
    jQuery(Faceted.Events).bind(Faceted.Events.FORM_DO_QUERY, function(evt, data){
      if(js_widget.operator != 'and' && (data.wid == js_widget.wid || data.wid == 'b_start')){
        return;
      }
      js_widget.count(sortcountable);
    });
  }
};

Faceted.CheckboxesWidget.prototype = {
  checkbox_click: function(element, evt){
    this.do_query(element);
  },

  do_query: function(element){
    this.selected = jQuery('input[type=checkbox]:checked', this.widget);
    var value = [];
    this.selected.each(function(i){
      value.push(jQuery(this).val());
    });
    Faceted.Form.do_query(this.wid, value);
  },

  reset: function(){
    // This is done by form.reset, so do nothing
    this.selected = [];
    jQuery(this.elements).attr('checked', false);
  },

  synchronize: function(){
    this.elements.attr('checked', false);
    var checked = Faceted.Query[this.wid];
    if(!checked){
      return;
    }

    jQuery('input[type=checkbox]', this.widget).val(checked);
    this.selected = jQuery('input[type=checkbox]:checked', this.widget);
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

    widget.selected.each(function(i){
      var span = jQuery('<span class="faceted-checkbox-criterion">')
      var element = jQuery(this);
      var id = element.attr('id');
      var value = element.val();
      var label = jQuery('label[for=' + id + ']', widget.widget);
      var title = label.attr('title');
      label = label.html();

      var link = jQuery('<a href="#">[X]</a>');
      link.attr('id', 'criteria_' + id);
      link.attr('title', 'Remove ' + title + ' filter');
      link.click(function(evt){
        widget.criteria_remove(value, element);
        return false;
      });

      span.append(link);
      span.append('<span>' + label + '</span>');
      html.append(span)
    });

    return html;
  },

  criteria_remove: function(value, element){
    // Remove all
    if(!value){
      this.elements.attr('checked', false);
      this.do_query();
    }else{
      element.attr('checked', false);
      this.do_query();
    }
  },

  count: function(sortcountable){
    var query = Faceted.SortedQuery();
    query.cid = this.wid;
    if(this.version){
      query.version = this.version;
    }
    if(this.operator){
      query.operator = this.operator;
    }

    var context = this;
    jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_START, {wid: context.wid});
    jQuery.getJSON(Faceted.BASEURL + '@@faceted_counter', query, function(data){
      context.count_update(data, sortcountable);
      jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_STOP, {wid: context.wid});
    });
  },

  count_update: function(data, sortcountable){
    var context = this;
    var lis = jQuery('li', context.widget);
    jQuery(lis).each(function(){
      var li = jQuery(this);
      li.removeClass('faceted-checkbox-item-disabled');
      li.removeClass('faceted-checkbox-item-zerocount');
      var input = jQuery('input', li);
      input.unbind();
      var key = input.val();

      var span = jQuery('span', li);
      if(!span.length){
        li.append(jQuery('<span>'));
        span = jQuery('span', li);
      }

      var value = data[key];
      value = value ? value : 0;
      span.text('(' + data[key] + ')');
      if(sortcountable){
        li.data('count', value);
      }
      if(!value){
        li.addClass('faceted-checkbox-item-disabled');
        if(context.widget.hasClass('faceted-zero-count-hidden')){
          li.addClass('faceted-checkbox-item-zerocount');
        }
        input.attr('disabled', 'disabled');
      }else{
        input.attr('disabled', false);
        input.click(function(evt){
          context.checkbox_click(this, evt);
        });
      }
    });
    if(sortcountable){
      lis.detach().sort(function(x, y) {
        var a = jQuery(x).data('count');
        var b = jQuery(y).data('count');
        return b - a;
      });
    }
    jQuery('ul', context.widget).append(lis);
    // Update expand/colapse
    context.fieldset.trigger('widget-refresh');
  }
};

Faceted.initializeCheckboxesWidget = function(evt){
  jQuery('div.faceted-checkboxes-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.CheckboxesWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeCheckboxesWidget);
});
