(function(jQuery) {
jQuery.fn.collapsible = function(settings){
  var self = this;
  self.colapsed = false;

  var options = {
    maxitems: 0,
    elements: 'li',

    events: {
      refresh: 'widget-refresh',
      expand: 'widget-expand',
      colapse: 'widget-colapse'
    },

    // Event handlers
    handle_refresh: function(evt, data){
      jQuery(options.elements, self).show();
      self.button.hide();

      if(!options.maxitems){
        return;
      }

      var elements = jQuery(options.elements, self);
      if(elements.length < options.maxitems){
        return;
      }

      if(self.colapsed){
        jQuery('a', self.button).text('More');
      }else{
        jQuery('a', self.button).text('Less');
      }
      self.button.show();

      if(!self.colapsed){
        return;
      }

      elements.each(function(index){
        if(index < options.maxitems){
          jQuery(this).show();
        }else{
          jQuery(this).hide();
        }
      });
    },

    handle_expand: function(evt, data){
      self.colapsed = false;
      self.trigger(options.events.refresh);
    },

    handle_colapse: function(evt, data){
      self.colapsed = true;
      self.trigger(options.events.refresh);
    },

    // Init
    initialize: function(){
      // Handle events
      self.bind(options.events.refresh, function(evt, data){
        options.handle_refresh(evt, data);
      });

      self.bind(options.events.expand, function(evt, data){
        options.handle_expand(evt, data);
      });

      self.bind(options.events.colapse, function(evt, data){
        options.handle_colapse(evt, data);
      });

      // More/Less button
      var link = jQuery('<a>').attr('href', '#').text('More');
      self.button = jQuery('<div>')
        .addClass('faceted-checkbox-more')
        .append(link)
        .hide();
      self.append(self.button);

      link.click(function(){
        if(self.colapsed){
          self.trigger(options.events.expand);
        }else{
          self.trigger(options.events.colapse);
        }
        return false;
      });

      if(options.maxitems){
        link.click();
      }
    }
  };

  if(settings){
    jQuery.extend(options, settings);
  }

  options.initialize();
  return this;

};
})(jQuery);
