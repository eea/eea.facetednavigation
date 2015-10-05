/* Alphabetical Widget
*/
Faceted.AlphabeticalWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();

  this.letters = jQuery('#' + wid + ' span');
  this.selected = [];

  // Faceted version
  this.version = '';
  var version = jQuery('#faceted-version');
  if(version){
    this.version = version.text();
  }

  // Set default value
  var selected = jQuery('.faceted_letter_selected');
  if(selected.length){
    Faceted.Query[this.wid] = [selected.attr('id').split('-')[1]];
    this.synchronize();
  }

  // Handle letter click
  var js_widget = this;
  this.letters.click(function(evt){
    js_widget.letter_click(this, evt);
  });

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
      if(data.wid == js_widget.wid || data.wid == 'b_start'){
        return;
      }
      js_widget.count(sortcountable);
    });
  }
};

Faceted.AlphabeticalWidget.prototype = {
  letter_click: function(letter, evt){
    this.do_query(letter);
  },

  letter_unselect: function(letter){
    jQuery(letter).removeClass('faceted_letter_selected');
    this.selected = [];
  },

  letter_select: function(letter){
    this.letter_unselect(this.letters);
    jQuery(letter).addClass('faceted_letter_selected');
    if(jQuery(letter).attr('id').split('-')[1] != 'all'){
      this.selected = [letter];
    }
  },

  do_query: function(letter){
    var value=jQuery(letter).attr('id').split('-')[1];
    var selected_value = '';
    if(this.selected.length){
      selected_value = jQuery(this.selected[0]).attr('id').split('-')[1];
    }
    if(value == selected_value){
      this.letter_select(jQuery('#' + this.wid + '-all'), this.widget);
      value = [];
    }else{
      this.letter_select(letter);
    }
    Faceted.Form.do_query(this.wid, value);
  },

  reset: function(){
    this.letter_select(jQuery('#' + this.wid + '-all', this.widget));
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
    }else{
      var letter = jQuery('#' + this.wid + '-' + value[0]);
      if(letter.length){
        this.letter_select(letter[0]);
      }else{
        this.reset();
      }
    }
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
      widget.criteria_remove(this, evt);
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
    var label=jQuery(this.selected[0]).attr('id').split('-')[1];
    var link = jQuery('<a href="#">[X]</a>');
    link.attr('id', 'criteria_' + this.wid + '_' + label);
    link.attr('title', 'Remove ' + label + ' filter');

    var widget = this;
    link.click(function(evt){
      widget.criteria_remove(this, evt);
      return false;
    });

    var html = jQuery('<dd>');
    html.attr('id', 'criteria_' + this.wid + '_entries');
    var span = jQuery('<span class="faceted-alphabetic-criterion">');
    span.append(link);
    jQuery('<span>').text(label).appendTo(span);
    html.append(span);
    return html;
  },

  criteria_remove: function(element, evt){
    this.do_query(this.selected[0]);
  },

  count: function(sortcountable){
    var query = Faceted.SortedQuery();
    query.cid = this.wid;
    if(this.version){
      query.version = this.version;
    }

    var context = this;
    jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_START, {wid: context.wid});
    jQuery.getJSON(Faceted.BASEURL + '@@faceted_counter', query, function(data){
      context.count_update(data, sortcountable);
      jQuery(Faceted.Events).trigger(Faceted.Events.DO_UPDATE);
      jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_STOP, {wid: context.wid});
    });
  },

  count_update: function(data, sortcountable){
    var context = this;
    context.letters.each(function(){
      var letter = jQuery(this);
      letter.removeClass('faceted-alphabetic-letter-disabled');
      letter.unbind();
      var key = letter.attr('id').split('-')[1];
      var value = data[key];
      value = value ? value : 0;
      letter.attr('title', value);
      if(sortcountable){
        letter.data('count', value);
      }
      if(!value){
        letter.addClass('faceted-alphabetic-letter-disabled');
      }else{
        letter.click(function(evt){
          context.letter_click(this, evt);
        });
      }
    });
    if(sortcountable){
      context.letters.detach().sort(function(x, y) {
        var a = jQuery(x).data('count');
        var b = jQuery(y).data('count');
        return b - a;
      });
    }
    jQuery('#' + context.wid, context.widget).append(context.letters);
  }
};

Faceted.initializeAlphabeticalWidget = function(evt){
  jQuery('div.faceted-alphabetic-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.AlphabeticalWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeAlphabeticalWidget);
});
