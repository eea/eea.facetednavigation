var Faceted = {version: '2.0'};
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
Faceted.Events.REDRAW = 'FACETED-REDRAW';
Faceted.Events.HASHCHANGE = 'hashchange.FACETED-HASHCHANGE';
Faceted.Events.DO_UPDATE = 'FACETED-DO_UPDATE';

/* Unbind events
*/
Faceted.Events.cleanup = function(){
  jQuery(Faceted.Events).unbind(Faceted.Events.AJAX_QUERY_START);
  jQuery(Faceted.Events).unbind(Faceted.Events.AJAX_QUERY_SUCCESS);
  jQuery(Faceted.Events).unbind(Faceted.Events.QUERY_INITIALIZED);
  jQuery(Faceted.Events).unbind(Faceted.Events.QUERY_CHANGED);
  jQuery(Faceted.Events).unbind(Faceted.Events.RESET);
  jQuery(Faceted.Events).unbind(Faceted.Events.FORM_DO_QUERY);
  jQuery(Faceted.Events).unbind(Faceted.Events.WINDOW_WIDTH_CHANGED);
  jQuery(Faceted.Events).unbind(Faceted.Events.WINDOW_HEIGHT_CHANGED);
  jQuery(Faceted.Events).unbind(Faceted.Events.AJAX_START);
  jQuery(Faceted.Events).unbind(Faceted.Events.AJAX_STOP);
  jQuery(Faceted.Events).unbind(Faceted.Events.AJAX_ERROR);
  jQuery(Faceted.Events).unbind(Faceted.Events.REDRAW);
  jQuery(Faceted.Events).unbind(Faceted.Events.DO_UPDATE);
  jQuery(window).unbind(Faceted.Events.HASHCHANGE); /* jQuery.bbq events */
};

/* Widgets
*/
Faceted.Widgets = {};

/* Query
*/
Faceted.Query = {};

/* Context url.
Default: (context related)
*/
Faceted.BASEURL = '';

/* UI Options
 */
Faceted.Options = {};
Faceted.Options.SHOW_SPINNER = true;
Faceted.Options.FADE_SPEED = 'slow';

/* Return minimal and sorted query
*/
Faceted.SortedQuery = function(query){
  if(!query){
    query = Faceted.Query;
  }

  var keys = [];
  jQuery.each(query, function(key){
    if(!this || this == 'all'){
      return;
    }
    keys.push(key);
  });

  keys.sort();
  var res = {};
  jQuery.each(keys, function(index){
    res[this] = query[this];
  });
  return res;
};

Faceted.Window = {
  initialize: function(){
    this.width = jQuery(window).width();
    this.height = jQuery(window).height();
    var js_window = this;
    jQuery(window).resize(function(){
      js_window.width_change();
      js_window.height_change();
    });

    // Full screen icon clicked
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
    this.mode = this.form.attr('data-mode') || 'view';

    // Faceted version
    this.version = '';
    var version = jQuery('#faceted-version', this.form);
    if(version){
      this.version = version.text();
    }

    // Handle errors
    this.area.ajaxError(function(event, request, settings){
      jQuery(this).html('' +
      '<h3>This site encountered an error trying to fulfill your request</h3>' +
      '<p>' +
        'If the error persists please contact the site maintainer. ' +
        'Thank you for your patience.' +
      '</p>');
      jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_ERROR);
    });

    var hashquery = Faceted.URLHandler.get();
    var has_hash = !jQuery.isEmptyObject(hashquery);

    if (has_hash) {
      Faceted.Query = hashquery;
    }

    if(Faceted.Query.b_start === undefined){
      Faceted.Query.b_start = 0;
    }

    if(this.mode === 'search' && !has_hash){
      /* if we are in search mode
       * and we don't have a request set up in URL
       * (this the case when we click 'back' button
       * we don't execute an initial search
       */
      return;
    }

    jQuery(Faceted.Events).trigger(Faceted.Events.QUERY_INITIALIZED);

    if(!has_hash){
      Faceted.URLHandler.set();
    }else{
      Faceted.URLHandler.hash_changed();
    }
  },

  initialize_paginator: function() {
    var context = this;
    Faceted.b_start_changed = false;
    jQuery('.listingBar a').each(function(i){
      jQuery(this).click(function(){
        var href = jQuery(this).attr('href');
        var regex = new RegExp('b_start\\:int=(\\d+)');
        var b_start = regex.exec(href)[1];
        Faceted.b_start_changed = true;
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
    if(wid != 'b_start' && !Faceted.b_start_changed){
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
    if(Faceted.Query.b_start === undefined){
      Faceted.Query.b_start = 0;
    }
    jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_QUERY_START);
    context.area.fadeOut('fast', function(){
      if(Faceted.Options.SHOW_SPINNER){
        var loading = '<div class="faceted_loading"><img src="' +
        Faceted.BASEURL + '++resource++faceted_images/ajax-loader.gif" /></div>';
        context.area.html(loading);
        context.area.fadeIn(Faceted.Options.FADE_SPEED);
      }

      var query = Faceted.SortedQuery();
      if(context.version){
        query.version = context.version;
      }
      jQuery.get(Faceted.BASEURL + '@@faceted_query', query, function(data){
        context.area.fadeOut('fast', function(){
          context.area.html(data);
          context.area.fadeIn(Faceted.Options.FADE_SPEED);
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
  },

  hash_changed: function(){
    Faceted.Query = this.get();
    jQuery(Faceted.Events).trigger(Faceted.Events.QUERY_CHANGED);
    Faceted.Form.do_form_query();
  },

  document_hash: function(){
    var r = window.location.href;
    var i = r.indexOf("#");
    return (i >= 0 ? r.substr(i+1) : '');
  },

  get: function(){
    var hash = jQuery.bbq.getState();
    var query = {};
    var types = ["number", "boolean", "string"];
    jQuery.each(hash, function(key, value){
      var value_type = typeof(value);
      if(jQuery.inArray(value_type, types) !== -1){
        value = [value];
      }
      query[key] = value;
    });
    return query;
  },

  set: function(query){
    if(!query){
      query = Faceted.Query;
    }
    query = jQuery.param(query, traditional=true);
    jQuery.bbq.pushState(query, 2);
  }
};

Faceted.Sections = {
  initialize: function(){
    var self = this;
    self.form = jQuery('.faceted-form');
    self.advanced = jQuery('.faceted-advanced-widgets', self.form).hide();
    if(!self.advanced.length){
      return;
    }

    self.buttons = jQuery('.faceted-sections-buttons', self.form);
    self.more = jQuery('.faceted-sections-buttons-more', self.form).show();
    self.less = jQuery('.faceted-sections-buttons-less', self.form).hide();

    jQuery('a', self.buttons).click(function(evt){
      self.toggle(jQuery(this), evt);
      return false;
    });
  },

  toggle: function(element, evt){
    this.more.toggle();
    this.less.toggle();
    this.advanced.toggle('blind');

    // Refresh tags facets
    var tags = jQuery('.faceted-tagscloud-widget:visible', this.form);
    if(tags.length){
      jQuery(Faceted.Events).trigger(Faceted.Events.WINDOW_WIDTH_CHANGED);
    }
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
    }
  },

  remove: function(wid){
    if(this.slaves.length){
      this.slaves = jQuery.map(this.slaves, function(slave, index){
        if(slave == wid){
          return null;
        }
        return slave;
      });
    }

    var widget = jQuery('#' + wid + '_widget');
    if(widget.length){
      widget.removeClass('faceted-widget-loading');
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

/* Load facetednavigation
*/
Faceted.Load = function(evt, baseurl){
  if(baseurl){
    Faceted.BASEURL = baseurl;
  }

  // Remove widgets with errors
  jQuery('.faceted-widget:has(div.faceted-widget-error)').remove();

  jQuery(Faceted.Events).bind(Faceted.Events.REDRAW, function(){
    if(jQuery('#faceted-left-column:has(div.faceted-widget)').length){
      jQuery('#center-content-area').addClass('left-area-js');
    }else{
      jQuery('#center-content-area').removeClass('left-area-js');
    }

    if(jQuery('#faceted-right-column:has(div.faceted-widget)').length){
      jQuery('#center-content-area').addClass('right-area-js');
    }else{
      jQuery('#center-content-area').removeClass('right-area-js');
    }
  });
  jQuery(Faceted.Events).trigger(Faceted.Events.REDRAW);

  // Init widgets UI
  jQuery(Faceted.Events).trigger(Faceted.Events.INITIALIZE);

  // Bind events
  jQuery(window).bind(Faceted.Events.HASHCHANGE, function(evt){
    Faceted.URLHandler.hash_changed();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt){
    Faceted.Form.initialize_paginator();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    Faceted.Form.reset();
  });

  Faceted.Window.initialize();
  Faceted.Sections.initialize();
  Faceted.AjaxLook.initialize();
  Faceted.Form.initialize();

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

/* Cleanup
*/
Faceted.Cleanup = function(){
  // Unbind events
  Faceted.Events.cleanup();

  // Reset
  Faceted.Widgets = {};
  Faceted.Query = {};

  // Reset URL hash
  Faceted.URLHandler.set();
};
