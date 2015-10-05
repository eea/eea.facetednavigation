/* Criteria Widget
*/
Faceted.CriteriaWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.title = jQuery('legend', this.widget).html();

  this.area = jQuery('#' + wid);
  this.reset_button = jQuery('#' + wid + '_reset');
  this.toggle_button = jQuery('.faceted-criteria-hide-show', this.widget);
  this.toggle_button_count = jQuery('.faceted-criteria-count', this.toggle_button);

  var js_widget = this;
  this.reset_button.click(function(evt){
    js_widget.reset_click(this, evt);
    return false;
  });

  var toggle_buttons = jQuery('a', this.toggle_button);
  toggle_buttons.click(function(evt){
    js_widget.toggle_button_click(this, evt);
    return false;
  });

  // Syndication
  js_widget.initialize_syndication();

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_START, function(evt){
    return js_widget.update();
  });

  jQuery(Faceted.Events).bind(Faceted.Events.DO_UPDATE, function(evt){
    return js_widget.update();
  });

  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    return js_widget.update_syndication();
  });
};

Faceted.CriteriaWidget.prototype = {
  reset_click: function(element, evt){
    jQuery(Faceted.Events).trigger(Faceted.Events.RESET);
    this.do_query();
  },

  toggle_button_click: function(element, evt){
    this.area.toggle('blind');
    jQuery('a', this.toggle_button).toggle();
    this.toggle_button_count.toggle();
  },

  do_query: function(wid, value){
    Faceted.Form.do_query(wid, value);
  },

  update: function(){
    var context = this;
    var empty=true;
    context.widget.fadeOut('fast', function(){
      context.area.empty();
      jQuery.each(Faceted.Query, function(key){
        var widget = Faceted.Widgets[key];
        if(!widget){
          return;
        }
        var criteria = widget.criteria();
        jQuery.each(criteria, function(){
          context.area.append(this);
          empty = false;
        });
      });

      var count = jQuery('dd span', context.area).length;
      context.toggle_button_count.text('(' + count + ')');

      if(!empty){
        context.widget.fadeIn('fast');
      }
    });
  },

  criteria: function(){
    return [];
  },

  initialize_syndication: function(){
    this.rss = null;
    this.rss_href = '';
    this.skos = null;
    this.skos_href = '';
    var icon = null;
    var rss = jQuery('#document-action-rss, #document-action-rss2').find('a');
    if(rss.length){
      rss = jQuery(rss[0]).clone();
      icon = jQuery('img', rss);
      icon.attr('id', icon.attr('id') + '-' + this.wid);
      rss.addClass('faceted-criteria-syndication-rss');
      rss.attr('id', this.wid + 'syndication-rss');
      jQuery('.faceted-criteria-reset', this.widget).prepend(rss);
      this.rss = jQuery('#' + this.wid + 'syndication-rss', this.widget);
      this.rss_href = rss.attr('href');
    }

    var skos = jQuery('#document-action-skos').find('a');
    if(skos.length){
      skos = jQuery(skos[0]).clone();
      icon = jQuery('img', skos);
      icon.attr('id', icon.attr('id') + '-' + this.wid);
      skos.addClass('faceted-criteria-syndication-skos');
      skos.attr('id', this.wid + 'syndication-skos');
      jQuery('.faceted-criteria-reset', this.widget).prepend(skos);
      this.skos = jQuery('#' + this.wid + 'syndication-skos', this.widget);
      this.skos_href = this.skos.attr('href');
    }
  },

  update_syndication: function(){
    var hash = 'ajax=True&';
    hash += Faceted.URLHandler.document_hash();
    if(this.rss){
      this.rss.attr('href', this.rss_href + '?' + hash);
    }

    if(this.skos){
      this.skos.attr('href', this.skos_href + '?' + hash);
    }
  }
};

Faceted.initializeCriteriaWidget = function(evt){
  jQuery('div.faceted-criteria-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.CriteriaWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeCriteriaWidget);
});
