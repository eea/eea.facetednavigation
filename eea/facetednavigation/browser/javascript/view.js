var Faceted = {version: '1.0.0'};
/* Events
*/
Faceted.Events = {};
Faceted.Events.INITIALIZE = 'FACETED-INITIALIZE';
Faceted.Events.AJAX_QUERY_START = 'FACETED-AJAX-QUERY-START';
Faceted.Events.AJAX_QUERY_SUCCESS = 'FACETED-AJAX-QUERY-SUCCESS';
Faceted.Events.QUERY_INITIALIZED = 'FACETED-QUERY-INITIALIZED';
Faceted.Events.QUERY_CHANGED = 'FACETED-QUERY-CHANGED';
Faceted.Events.RESET = 'FACETED-RESET';
Faceted.Events.FORM_DO_QUERY = 'FACETED-FORM-DO-QUERY';
Faceted.Events.WINDOW_WIDTH_CHANGED = 'FACETED-WINDOW-WIDTH-CHANGED';
Faceted.Events.WINDOW_HEIGHT_CHANGED = 'FACETED-WINDOW-HEIGHT-CHANGED';
Faceted.Events.AJAX_START = 'FACETED-AJAX-START';
Faceted.Events.AJAX_STOP = 'FACETED-AJAX-STOP';
Faceted.Events.AJAX_ERROR = 'FACETED-AJAX-ERROR';

/* Widgets
*/
Faceted.Widgets = {};

/* Query
*/
Faceted.Query = {};

Faceted.Window = {
  initialize: function(){
    this.width = jQuery(window).width();
    this.height = jQuery(window).height();
    var js_window = this;
    jQuery(window).resize(function(){
      js_window.width_change();
      js_window.height_change();
    });

    // Full screen icon cliked
    var fullscreen = jQuery('a:has(img#icon-full_screen)');
    if(fullscreen.length){
      js_window.toggle_fullscreen(fullscreen);
    }
  },

  width_change: function(){
    var width = jQuery(window).width();
    if(width != this.width){
      this.width = width;
      jQuery(Faceted.Events).trigger(
        Faceted.Events.WINDOW_WIDTH_CHANGED, {width: width}
      );
    }
  },

  height_change: function(){
    var height = jQuery(window).height();
    if(height != this.height){
      this.height = height;
      jQuery(Faceted.Events).trigger(
        Faceted.Events.WINDOW_HEIGHT_CHANGED, {height: height}
      );
    }
  },

  toggle_fullscreen: function(button){
    button.attr('href', '#');
    button.click(function(evt){
      var toggleFullScreenMode = window.toggleFullScreenMode;
      if(toggleFullScreenMode){
        toggleFullScreenMode();
        jQuery(Faceted.Events).trigger(Faceted.Events.WINDOW_WIDTH_CHANGED);
      }
      return false;
    });
  }
};

/*
  @class Faceted.Form
*/
Faceted.Form = {
  initialize: function(){
    this.form = jQuery('#faceted-form');
    // Handle form submit event
    this.area = jQuery('#faceted-results');

    // Handle errors
    this.area.ajaxError(function(event, request, settings){
      jQuery(this).html('<h3>This site encountered an error trying to fulfill your request</h3><p>If the error persists please contact the site maintainer. Thank you for your patience.</p>');
      jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_ERROR);
    });

    var query = Faceted.URLHandler.get();
    // if(!query) -> false always
    for(var name in query){
      Faceted.Query = query;
      break;
    }
    jQuery(Faceted.Events).trigger(Faceted.Events.QUERY_INITIALIZED);
    Faceted.URLHandler.set();
  },

  initialize_paginator: function() {
    var context = this;
    jQuery('.listingBar a').each(function(i){
      jQuery(this).click(function(){
        var href = jQuery(this).attr('href');
        var regex = new RegExp('b_start\\:int=(\\d+)');
        var b_start = regex.exec(href)[1];
        context.do_query('b_start', b_start);
        return false;
      });
    });
  },

  reset: function(evt){
    Faceted.Query = {};
  },

  do_query: function(wid, value){
    // Update query
    if(wid != 'b_start'){
      Faceted.Query.b_start = 0;
    }
    if(!value){
      value = [];
    }
    if(wid){
      Faceted.Query[wid] = value;
    }

    jQuery(Faceted.Events).trigger(Faceted.Events.FORM_DO_QUERY, {wid: wid});
    // Update url
    Faceted.URLHandler.set();
  },

  do_form_query: function(){
    var context = this;
    if(!Faceted.Query.b_start){
      Faceted.Query.b_start = 0;
    }

    jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_QUERY_START);
    context.area.fadeOut('fast', function(){
      var loading = '<div class="faceted_loading"><img src="++resource++faceted_images/ajax-loader.gif" /></div>';
      context.area.html(loading);
      context.area.fadeIn('slow');
      jQuery.get('@@faceted_query', Faceted.Query, function(data){
        context.area.fadeOut('fast', function(){
          context.area.html(data);
          context.area.fadeIn('slow');
          jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_QUERY_SUCCESS);
        });
      });
    });
  },
  /* Errors
  */
  highlight: function(elements, css_class, remove){
    for(var i=0;i<elements.length;i++){
      var element = jQuery('#' + elements[i]);
      if(remove){
        jQuery(element).removeClass(css_class);
      }else{
        jQuery(element).addClass(css_class);
      }
    }
  },

  raise_error: function(msg, error_area, highlights){
    var area = jQuery('#' + error_area);
    msg = '<div class="portalMessage">' + msg + '</div>';
    area.html(msg);
    this.highlight(highlights, 'error');
  },

  clear_errors: function(error_area, highlights){
    var area = jQuery('#' + error_area);
    area.html('');
    this.highlight(highlights, 'error', true);
  }
};

Faceted.URLHandler = {
  initialize: function(){
    this.hash = null;
    this.iframe = null;

    if (jQuery.browser.msie && jQuery.browser.version < 8){
      var iframe = jQuery('<iframe>');
      iframe.attr('id', 'faceted-iehistory');
      var iediv = jQuery('<div>');
      iediv.css('display', 'none');
      iediv.html(iframe);
      jQuery('#faceted-form').append(iediv);
      this.iframe = jQuery('#faceted-iehistory');
      var ie_hash = this.query2hash(Faceted.Query);
      this.iframe.attr('src', '@@faceted_history?' + ie_hash.replace('#', ''));
    }
  },

  hash_changed: function(){
    if(this.iframe){
      return this.ie_hash_changed();
    }else{
      return this.other_hash_changed();
    }
  },

  ie_hash_changed: function(){
    try{
      var history = jQuery('#faceted-ie-history-hash', this.iframe[0].contentWindow.document);
      var ie_hash = history.text();
    }catch(exception){
      // IE 7 history not initialized yet, do nothing.
      return;
    }

    if(this.hash != ie_hash){
      this.hash = ie_hash;
      document.location.hash = this.hash;

      Faceted.Query = this.hash2query(this.hash);
      jQuery(Faceted.Events).trigger(Faceted.Events.QUERY_CHANGED);
      Faceted.Form.do_form_query();
    }
  },

  other_hash_changed: function(){
    if(document.location.hash != this.hash){
      this.hash = document.location.hash;

      Faceted.Query = this.hash2query(this.hash);
      jQuery(Faceted.Events).trigger(Faceted.Events.QUERY_CHANGED);
      Faceted.Form.do_form_query();
    }
  },

  document_hash: function(){
    var r = window.location.href;
    var i = r.indexOf("#");
    return (i >= 0 ? r.substr(i+1) : '');
  },

  get: function(){
    var hash = document.location.hash;
    hash = hash.replace('#', '');
    return this.hash2query(hash);
  },

  set: function(query){
    if(!query){
      query = Faceted.Query;
    }
    var hash = this.query2hash(query);
    if(!this.iframe){
      document.location.hash = hash;
    }else{
      hash = hash.replace('#', '');
      this.iframe.attr('src', '@@faceted_history?' + hash);
    }
  },

  hash2query: function(hash){
    hash = hash.replace('#', '');
    var items = hash.split('&');
    var query = {};
    jQuery.each(items, function(i){
      var item = this.split('=');
      var key = item[0];
      var value = item[1];
      if(!value){
        return;
      }
      if(value.indexOf('+')!=-1){
        value = value.replace(/\+/g, ' ');
      }
      if(!query[key]){
        query[key] = [value];
      }else{
        query[key].push(value);
      }
    });
    return query;
  },

  query2hash: function(query){
    var hash = '#';
    hash += jQuery.param(query);
    return hash;
  }
};

Faceted.Sections = {
  initialize: function(){
    this.init_sections();
  },

  init_sections: function(){
    var sections = jQuery('div.faceted-column:has(.faceted-section-header)');
    sections.each(function(){
      var section = jQuery(this);
      var headers = jQuery('.faceted-section-header', section);
      headers.show();

      section.accordion({
        autoHeight: false
      });

      section.bind('accordionchange', function(evt, ui){
        var tags = jQuery('.faceted-tagscloud-widget:visible', section);
        if(!tags.length){
          return;
        }
        jQuery(Faceted.Events).trigger(Faceted.Events.WINDOW_WIDTH_CHANGED);
      });

    });
  }
};

Faceted.AjaxLook = {
  initialize: function(){
    this.slaves = [];
    this.locked = false;
    // Events
    var js_object = this;
    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_START, function(evt, data){
      js_object.add(data.wid);
    });

    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_STOP, function(evt, data){
      js_object.remove(data.wid);
    });

    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_START, function(evt){
      js_object.add('faceted-results');
    });

    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt){
      js_object.remove('faceted-results');
    });

    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_ERROR, function(evt){
      jQuery(this.slaves).each(function(index){
        js_object.remove(js_object.slaves[index]);
      });
    });
  },

  add: function(wid){
    this.lock();
    this.slaves.push(wid);

    var widget = jQuery('#' + wid + '_widget');
    if(widget.length){
      widget.addClass('faceted-widget-loading');
      if(jQuery.browser.msie){
        widget.addClass('faceted-widget-loading-msie');
      }
    }
  },

  remove: function(wid){
    if(this.slaves.length){
      var index = jQuery(this.slaves).index(wid);
      if(index != -1){
        this.slaves.splice(index, 1);
      }
    }

    var widget = jQuery('#' + wid + '_widget');
    if(widget.length){
      widget.removeClass('faceted-widget-loading');
      widget.removeClass('faceted-widget-loading-msie');
    }
    this.unlock();
  },

  lock: function(){
    if(this.locked){
      // Already locked
      return;
    }
    this.locked = true;
    jQuery.each(Faceted.Widgets, function(key){
      this.widget.addClass('faceted-widget-locked');
    });

    var overlay = jQuery('<div>');
    overlay.addClass('faceted-lock-overlay');
    overlay.addClass('ui-widget-overlay');
    overlay.css('z-index', 1001);
    jQuery('#faceted-form').append(overlay);
  },

  unlock: function(){
    if(this.slaves.length){
      return;
    }
    this.locked = false;

    jQuery.each(Faceted.Widgets, function(key){
      this.widget.removeClass('faceted-widget-locked');
    });

    jQuery('.faceted-lock-overlay').remove();
  }
};

/* Document ready
*/
Faceted.Load = function(){
  if(jQuery('#faceted-left-column:has(div)').length){
    jQuery('#center-content-area').addClass('left-area-js');
  }

  if(jQuery('#faceted-right-column:has(div)').length){
    jQuery('#center-content-area').addClass('right-area-js');
  }

  // Init widgets UI
  jQuery(Faceted.Events).trigger(Faceted.Events.INITIALIZE);

  Faceted.Form.initialize();
  Faceted.URLHandler.initialize();
  Faceted.Window.initialize();
  Faceted.Sections.initialize();
  Faceted.AjaxLook.initialize();

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt){
    Faceted.Form.initialize_paginator();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    Faceted.Form.reset();
  });

  setInterval("Faceted.URLHandler.hash_changed()", 300);
  // Override calendar close handler method in order to raise custom events
  if(window.Calendar){
    Calendar.prototype.callCloseHandler = function () {
      // Original code
      if (this.onClose) {
        this.onClose(this);
      }
      this.hideShowCovered();
      // Custom events
      var wid = this.params.inputField.id;
      wid = wid.split('_')[2];
      if(!wid){
        return false;
      }

      var widget = Faceted.Widgets[wid];
      widget.do_query();
      return false;
    };
  }
};

Faceted.Unload = function(){
};
