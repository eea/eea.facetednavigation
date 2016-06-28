var FacetedEdit = {version: '2.0'};
FacetedEdit.loading = '<div class="faceted_loading"><img src="++resource++faceted_images/ajax-loader.gif" /></div>';

// Widgets
FacetedEdit.Widgets = {};

/* Context url.
Default: (context related)
*/
FacetedEdit.BASEURL = '';

// Events
FacetedEdit.Events = {};
FacetedEdit.Events.RELOAD_WIDGETS = 'FACETEDEDIT-RELOAD-WIDGETS';
FacetedEdit.Events.INITIALIZE_WIDGETS = 'FACETEDEDIT-INITIALIZE-WIDGETS';
FacetedEdit.Events.POSITION_UPDATED = 'FACETEDEDIT-POSITION-UPDATED';
FacetedEdit.Events.WINDOW_WIDTH_CHANGED = 'FACETEDEDIT-WINDOW-WIDTH-CHANGED';
FacetedEdit.Events.WINDOW_HEIGHT_CHANGED = 'FACETEDEDIT-WINDOW-HEIGHT-CHANGED';
FacetedEdit.Events.AJAX_START = 'FACETEDEDIT-AJAX-START';
FacetedEdit.Events.AJAX_STOP = 'FACETEDEDIT-AJAX-STOP';
FacetedEdit.Events.CATALOG_CHANGED = 'FACETEDEDIT-CATALOG-CHANGED';

FacetedEdit.Window = {
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
      jQuery(FacetedEdit.Events).trigger(
        FacetedEdit.Events.WINDOW_WIDTH_CHANGED, {width: width}
      );
    }
  },

  height_change: function(){
    var height = jQuery(window).height();
    if(height != this.height){
      this.height = height;
      jQuery(FacetedEdit.Events).trigger(
        FacetedEdit.Events.WINDOW_HEIGHT_CHANGED, {height: height}
      );
    }
  },

  toggle_fullscreen: function(button){
    button.attr('href', '#');
    button.click(function(evt){
      var toggleFullScreenMode = window.toggleFullScreenMode;
      if(toggleFullScreenMode){
        toggleFullScreenMode();
        jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.WINDOW_WIDTH_CHANGED);
      }
      return false;
    });
  }
};

FacetedEdit.FormMessage = {
  initialize: function(){
    var js_obj = this;
    // Add portal status message
    var context = jQuery('#faceted-edit-widgets-ajax');
    var msg = jQuery('<dl>')
      .addClass('portalMessage')
      .attr('id', 'faceted-portal-status-message')
      .css({
        float: 'left',
        cursor: 'pointer',
        margin: '0px',
        width: '80%',
        'text-align': 'left'
      }).append(jQuery('<dt>').text('Info'));

    var msg_area = jQuery('<dd>')
      .attr('id', 'faceted-portal-status-message-area');

    var msg_close = jQuery('<span>')
      .addClass('ui-icon')
      .addClass('ui-icon-close')
      .attr('title', 'Close message')
      .html(' ')
      .css({
        float: 'right',
        margin: '0.5em'
      });

    msg.click(function(){
      js_obj.msg.hide();
    });
    msg.append(msg_close).append(msg_area);
    context.prepend(msg);
    this.msg = msg;
    this.msg_area = msg_area;
    this.msg.hide();

    var lock = jQuery('<div>');
    lock.attr('id', 'faceted-portal-status-message-lock');
    lock.css('margin', '0px');
    context.prepend(lock);
    this.lock = jQuery('#faceted-portal-status-message-lock', context);

    this.lock.dialog({
      modal: true,
      closeOnEscape: false,
      autoOpen: false,
      draggable: false,
      resize: false,
      dialogClass: 'faceted-loading-overlay'
    });
    this.lock.html(FacetedEdit.loading);

    // Events
    jQuery(FacetedEdit.Events).bind(FacetedEdit.Events.AJAX_START, function(evt, data){
      js_obj.start(data.msg);
    });
    jQuery(FacetedEdit.Events).bind(FacetedEdit.Events.AJAX_STOP, function(evt, data){
      js_obj.stop(data.msg);
    });
  },

  start: function(msg){
    this.lock.dialog('open');
    this.update(msg);
  },

  stop: function(msg){
    this.lock.dialog('close');
    this.update(msg);
  },

  update: function(msg){
    this.msg_area.html(msg);
    if(!msg){
      this.msg.hide();
    }else{
      this.msg.show();
    }
  },

  custom_message: function(text, area){
    var msg = jQuery('#' + area + ' .faceted-add-widget-dialog-msg');
    if(!msg.length){
      var loading_text = jQuery('<span>');
      loading_text.attr('class', 'portalMessage faceted-add-widget-dialog-msg');
      loading_text.css('display', 'none');
      loading_text.html(text);
      jQuery('#' + area).append(loading_text);
    }
    msg = jQuery('#' + area + ' .faceted-add-widget-dialog-msg');
    msg.fadeIn('slow', function(){
      msg.fadeOut('slow');
    });
  }
};

FacetedEdit.FormPosition = {
  initialize: function(){
    this.query = {};
  },

  submit: function(action){
    this.update();
    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(action, this.query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.POSITION_UPDATED);
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  },

  update: function(){
    var context = this;
    context.query = {};
    context.query.redirect = '';
    context.query.updatePosition_button = 'Change';

    var positions = jQuery('#wposition option');
    positions.each(function(){
      var pos_val = jQuery(this).val();
      context.query[pos_val] = [];

      var widgets = jQuery('#faceted-' + pos_val + '-column div.faceted-widget');
      widgets.each(function(){
        var wid = jQuery(this).attr('id').split('_')[0];
        context.query[pos_val].push(wid);
      });
    });
  }
};

FacetedEdit.FormWidgets = {
  initialize: function(){
    this.form = jQuery('#faceted-edit-widgets');
    this.form.ajaxError(function(event, request, settings){
      jQuery(this).html('<h3>This site encountered an error trying to fulfill your request</h3><p>If the error persists please contact the site maintainer. Thank you for your patience.</p>');
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: 'Error'});
    });
    jQuery('.faceted-edit-fieldset').hide();
    this.action = this.form.attr('action');
    this.form.css('display', 'block');
    this.form.css('clear', 'both');
    this.form.html(FacetedEdit.loading);
    this.update();

    // Confirm delete dialog
    var js_obj = this;
    jQuery('#confirm-delete-dialog').dialog({
      bgiframe: true,
      autoOpen: false,
      modal: true,
      buttons:  {
        Yes: function() {
          var label = jQuery('strong', jQuery(this));
          var wid = label.attr('id');
          var cid = wid.split('_')[0];
          jQuery('#' + wid).slideUp(function(){
            js_obj.delete_widget(cid);
            jQuery('#' + wid).remove();
          });
          jQuery(this).dialog('close');
        },
        No: function() {
          jQuery(this).dialog('close');
        }
      }
    });

    // Events
    jQuery(FacetedEdit.Events).bind(FacetedEdit.Events.RELOAD_WIDGETS, function(evt, data){
      js_obj.update();
    });
  },

  update: function(){
    var context = this;
    var nocache = new Date();
    nocache = nocache.getTime();

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Refreshing ...'});
    jQuery.get(FacetedEdit.BASEURL + '@@faceted_widgets', {nocache: nocache}, function(data){
      context.form.html(data);

      jQuery('#faceted-results').html(context.background_text(
        'Results here', {'padding-top': '2em', 'padding-bottom': '2em'}
      ));

      jQuery('div.faceted-widget').show();

      jQuery('.faceted-drag-drop').sortable({
        items: '.faceted-widget',
        connectWith: '.faceted-drag-drop',
        placeholder: 'ui-state-highlight',
        forcePlaceholderSize: true,
        opacity: 0.7,
        delay: 300,
        cursor: 'crosshair',
        tolerance: 'pointer',
        update: function(event, ui){
          if(!ui.sender){
            var parent = ui.item.parent();
            if(jQuery(parent).hasClass('faceted-widgets')){
              FacetedEdit.FormPosition.submit(context.action);
            }
          }
        }
      });

      jQuery('.faceted-widgets .ui-widget-header').disableSelection();
      jQuery('div.faceted-widget').dblclick(function(){
        var wid = jQuery(this).attr('id');
        context.edit_widget(wid);
      });

      jQuery('div.faceted-widget input[type=submit]').click(function(){
        return false;
      });
      jQuery('div.faceted-widget a').click(function(){
        return false;
      });

      // Add widget buttons
      var addbutton = jQuery('<span>');
      addbutton.attr('title', 'Add widget here');
      addbutton.text(' + ');
      addbutton.attr('class', 'ui-icon ui-icon-plus ui-corner-all');
      jQuery('.faceted-widgets').each(function(){
        var container = jQuery(this);
        var container_id = container.attr('id').split('---');
        var position = container_id[0];
        var section = container_id[1];
        var local_addbutton = addbutton.clone();
        local_addbutton.click(function(evt){
          var dialog = jQuery('#faceted-edit-addwidget');
          jQuery('#wposition', dialog).val(position);
          jQuery('#wsection', dialog).val(section);
          dialog.dialog('open');
          FacetedEdit.FormAddWidgets.wtype_update(
            FacetedEdit.FormAddWidgets.wtype.val());
          return false;
        });
        var div = jQuery('<div>');
        div.addClass('faceted-add-button');
        div.append(local_addbutton);
        container.prepend(div);
      });

      // Make portlets
      jQuery('.faceted-widget').each(function(){
        var wid = jQuery(this).attr('id');
        jQuery(this).attr('title', 'Click and drag to change widget position');
        var cid = wid.split('_')[0];
        var legend = jQuery('#' + wid + ' legend');
        legend.hide();

        // Widget header
        var header = jQuery('<div>');
        header.attr('class', 'ui-widget-header');

        // Delete widget button
        var header_del_button = jQuery('<div>');
        header_del_button.attr('title', 'Delete widget');
        header_del_button.css('float', 'right');
        header_del_button.attr('class', 'ui-icon ui-icon-trash');
        header_del_button.html('x');
        header_del_button.click(function(){
          var confirm = jQuery('#confirm-delete-dialog');
          var label = jQuery('strong', confirm);
          label.attr('id', wid);
          label.text(legend.text());
          jQuery('#confirm-delete-dialog').dialog('open');
        });

        // Edit widget button
        var header_edit_button = jQuery('<div>');
        header_edit_button.attr('title', 'Edit widget');
        header_edit_button.css('float', 'right');
        header_edit_button.attr('class', 'ui-icon ui-icon-pencil');
        header_edit_button.html('e');
        header_edit_button.click(function(){
          context.edit_widget(cid);
        });

        // Hide/show widget button
        var header_hide_button = jQuery('<div>');
        var css = 'ui-icon-hide';
        if(jQuery('#' + wid).hasClass('faceted-widget-hidden')){
          header_hide_button.attr('title', 'Show widget');
          css = 'ui-icon-show';
        }else{
          header_hide_button.attr('title', 'Hide widget');
        }
        header_hide_button.css('float', 'right');
        header_hide_button.attr('class', 'ui-icon');
        header_hide_button.addClass(css);
        header_hide_button.html('h');
        header_hide_button.click(function(){
          context.hide_button_click(wid, cid);
        });

        // Widget title
        var header_legend = jQuery('<div>');
        header_legend.html(legend.html());

        header.append(header_del_button);
        header.append(header_edit_button);
        header.append(header_hide_button);
        header.append(header_legend);
        legend.after(header);
      });

      FacetedEdit.Widgets = {};
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.INITIALIZE_WIDGETS);
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: 'Interface refreshed'});
    });
  },

  background_text: function(text, css){
    var div = jQuery('<div>');
    div.html(text);
    div.attr('class', 'faceted-empty-column');
    if(css){
      div.css(css);
    }
    return div;
  },

  delete_widget: function(criterion_id){
    var context = this;
    var query = {};
    query.path = criterion_id;
    query.deleteWidget_button = 'Delete';
    query.redirect = '';
    jQuery.post(this.action, query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  },

  edit_widget: function(widget_id){
    FacetedEdit.FormEditWidget.edit(widget_id);
  },

  hide_button_click: function(widget_id, criterion_id){
    var widget = jQuery('#' + widget_id);
    var button = jQuery('#' + widget_id + ' div.ui-icon-hide, div.ui-icon-show');
    var action = FacetedEdit.BASEURL + '@@faceted_configure';
    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = criterion_id;

    if(widget.hasClass('faceted-widget-hidden')){
      this.show_widget(widget_id);
      query['faceted.' + criterion_id + '.hidden-empty-marker'] = 1;
    }else{
      this.hide_widget(widget_id);
      query['faceted.' + criterion_id + '.hidden'] = 'selected';
    }

    jQuery.post(action, query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  },

  hide_widget: function(widget_id){
    var widget = jQuery('#' + widget_id);
    var button = jQuery('#' + widget_id + ' div.ui-icon-hide');
    button.attr('title', 'Show widget');
    button.removeClass('ui-icon-hide');
    button.addClass('ui-icon-show');
    jQuery('#' + widget_id).addClass('faceted-widget-hidden');
  },

  show_widget: function(widget_id){
    var widget = jQuery('#' + widget_id);
    var button = jQuery('#' + widget_id + ' div.ui-icon-show');
    button.attr('title', 'Hide widget');
    button.removeClass('ui-icon-show');
    button.addClass('ui-icon-hide');
    jQuery('#' + widget_id).removeClass('faceted-widget-hidden');
  }
};

FacetedEdit.FormEditWidget = {
  initialize: function(){
    this.query = '';
    this.cid = null;
    var context = this;
    var form = jQuery('.faceted-edit-widget-dialog');
    if(!form.length){
      form = jQuery('<form>');
      form.attr('class', 'faceted-edit-widget-dialog');
      form.attr('title', 'Edit widget');
      form.attr('id', 'faceted-edit-widget-dialog');
      jQuery('#faceted-edit-widgets-ajax').append(form);
    }
    this.form = jQuery('.faceted-edit-widget-dialog');
    this.form.dialog({
      bgiframe: true,
      modal: true,
      autoOpen: false,
      buttons: {
        'Save': function(){
          var valid = FacetedEdit.FormValidator.validate(context.form);
          if(valid){
            context.submit();
            jQuery(this).dialog('close');
          }
        },
        'Cancel': function(){
          jQuery(this).dialog('close');
        }
      },
      close: function(){
        FacetedEdit.FormValidator.clear(context.form);
        context.form.html("");
      }
    });
  },

  edit: function(widget_id){
    var context = this;
    context.cid = widget_id.split('_')[0];
    var query = {};
    query.criterion = widget_id;

    context.form.html(FacetedEdit.loading);
    context.form.dialog('open');
    jQuery.get(FacetedEdit.BASEURL + '@@faceted_schema', query, function(data) {
      context.form.html(data);

      //jQuery('.field-c0-form-c0-default').remove();
      var selector = '.field-' + context.cid + '-faceted-' + context.cid;
      jQuery(selector + '-default').remove();

      var catalog = jQuery(selector + '-index select');
      var operator = jQuery(selector + '-operator select');
      if(catalog.length && operator.length){
        operator = operator.clone();
        jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.CATALOG_CHANGED, {
          catalog: catalog,
          operator: operator
        });
        catalog.change(function(){
          jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.CATALOG_CHANGED, {
            catalog: catalog,
            operator: operator
          });
        });
      }
      var widget = jQuery('.faceted-widget-edit', context.form);
      jQuery('ul', widget).addClass('formTabs').show();
      jQuery('li', widget).addClass('formTab');
      jQuery('ul', widget).tabs('div.panes > div');
    });
  },

  submit: function(){
    var context = this;
    var action = FacetedEdit.BASEURL + '@@faceted_configure';
    this.update_query();
    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(action, this.query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.RELOAD_WIDGETS, {msg: data});
    });
    return false;
  },

  update_query: function(){
    this.query = 'cid=' + this.cid;
    this.query += '&redirect=&updateCriterion_button=Save&';
    this.query += this.form.serialize();
  }
};

FacetedEdit.FormAddWidgets = {
  initialize: function(){
    this.query = '';
    this.form = jQuery('#faceted-edit-addwidget');
    var context = this;
    jQuery('#faceted-edit-addwidget').dialog({
      bgiframe: true,
      modal: true,
      autoOpen: false,
      buttons: {
        'Add': function(){
          var valid = FacetedEdit.FormValidator.validate(context.form);
          if(valid){
            context.submit(context.form);
            jQuery(this).dialog('close');
          }
        },
        'Cancel': function(){
          jQuery(this).dialog('close');
        }
      },
      close: function(){
        FacetedEdit.FormValidator.clear(context.form);
        context.details.html("");
      }
    });
    this.wtype = jQuery('#wtype');

    this.details = jQuery('#faceted-widget-details');

    // Events
    this.form.submit(function(evt){
      return context.submit(context.form, evt);
    });
    this.wtype.change(function(evt){
      return context.wtype_change(this, evt);
    });

    jQuery('#faceted-edit-addwidget input[type=submit]').hide();
    jQuery('#faceted-field-wposition').hide();
    jQuery('#faceted-field-wsection').hide();
    jQuery('#faceted-widget-type .field', this.form).css('float', 'left');
    var clear = jQuery('<div>');
    clear.html('&nbsp;');
    clear.css('clear', 'both');
    jQuery('#faceted-widget-type', this.form).after(clear);
  },

  wtype_change: function(element, evt){
    FacetedEdit.FormValidator.clear(this.form);
    this.wtype_update(jQuery(element).val());
  },

  wtype_update: function(widget_type){
    var faceted_query = {};
    faceted_query.criterion = 'addformcriterion_widget';
    faceted_query.widget = widget_type;
    var context = this;

    jQuery.get(FacetedEdit.BASEURL + '@@faceted_schema', faceted_query, function(data) {
      FacetedEdit.FormMessage.custom_message('Loading...', 'faceted-widget-type');
      context.details.html(data);
      var selector = '.field-c0-faceted-c0';
      jQuery(selector + '-default').hide();
      var catalog = jQuery(selector + '-index select');
      var operator = jQuery(selector + '-operator select');
      if(catalog.length && operator.length){
        operator = operator.clone();
        catalog.change(function(){
          jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.CATALOG_CHANGED, {
            catalog: catalog,
            operator: operator
          });
        });
      }
      jQuery('#c0-layout-header').remove();
      jQuery('#c0-layout-tab').remove();
      var widget = jQuery('.faceted-widget-edit', context.details);
      jQuery('ul', widget).attr('class', 'formTabs').show();
      jQuery('li', widget).attr('class', 'formTab');
      jQuery('ul', widget).tabs('div.panes > div');
    });
  },

  submit: function(form, evt){
    this.update_query();

    var context = this;
    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Adding ...'});
    jQuery.post(form.attr('action'), this.query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.RELOAD_WIDGETS, {msg: data});
    });
    return false;
  },

  update_query: function(){
    this.query = 'redirect=&addPropertiesWidget_button=Add&';
    this.query += this.form.serialize();
    console.log(this.query);
  }
};

FacetedEdit.FormImportExport = {
  initialize: function(){
    jQuery('.faceted-exportimport-fieldset').hide();
    this.form = jQuery('.faceted-exportimport-fieldset form');
    this.form.submit(function(){
      return false;
    });

    var context = this;
    var buttons = jQuery('input[type=submit]', this.form);
    buttons.each(function(){
      var button = jQuery(this);
      var new_button = button.clone();
      new_button.click(function(){
        if(new_button.attr('name') == 'export_button'){
          context.export_xml();
        }
      });
      jQuery('#faceted-edit-widgets-ajax').prepend(new_button);
      button.remove();
    });

    var import_button = jQuery('#import_button');
    import_button.css('cursor', 'pointer');
    var upload = new AjaxUpload(import_button, {
      action: this.form.attr('action'),
      name: 'import_file',
      data: {
        redirect: '',
        import_button: 'Import'
      },
      autoSubmit: true,
      onComplete: function(file, response) {
        var data = jQuery(response);
        jQuery(FacetedEdit.Events).trigger(
          FacetedEdit.Events.RELOAD_WIDGETS, {msg: data.text()
        });
      }
    });
  },

  export_xml: function(){
    var query = {};
    query.redirect = '';
    query.export_button = 'Export';
    var action = this.form.attr('action');
    action += '?' + jQuery.param(query);
    return window.open(action, '_blank');
  }
};

FacetedEdit.FormValidator = {
  validate: function(form){
    this.clear();

    var error = jQuery('<div>');
    error.attr('class', 'dialog-error-header ui-state-error ui-corner-all');
    error.attr('id', 'form-validator-errors');
    form.prepend(error);

    var valid = true;
    valid = valid && this.validate_numbers(form);
    valid = valid && this.validate_integers(form);
    valid = valid && this.validate_required(form);
    return valid;
  },

  validate_numbers: function(form){
    var inputs = jQuery('#' + jQuery(form).attr('id') + ' input[type=text]');
    var valid = true;
    var context = this;
    jQuery.each(inputs, function(){
      var input = jQuery(this);
      if(jQuery(this).attr('name').indexOf(':int')==-1){
        return;
      }
      var value = input.val();
      value = parseInt(value, 10);
      if(value || value === 0){
        input.val(value);
      }else{
        input.addClass('ui-state-error');
        context.error_message(form, input, 'Invalid number');
        valid = false;
      }
    });
    return valid;
  },

  validate_integers: function(form){
    var valid = true;
    var elements = jQuery('.ArchetypesIntegerWidget :input[type=text]', form);
    var context = this;
    elements.each(function(){
      var input = jQuery(this);
      var value = input.val();
      value = parseInt(value, 10);
      if(value || value === 0){
        input.val(value);
      }else{
        input.addClass('ui-state-error');
        context.error_message(form, input, 'Invalid number');
        valid = false;
      }
    });
    return valid;
  },

  validate_required: function(form){
    var valid = true;
    var elements = jQuery('div.field:has(span.required) :input', jQuery(form));

    var context = this;
    jQuery.each(elements, function(){
      var element = jQuery(this);
      var value = element.val();
      if(!value){
        element.addClass('ui-state-error');
        context.error_message(form, element, 'Value required');
        valid = false;
      }
    });
    return valid;
  },

  error_message: function(form, element, msg){
    var error = jQuery('#form-validator-errors');
    var message = jQuery('<span>');
    message.attr('class', 'ui-icon ui-icon-alert');
    message.css({'float': 'left', 'margin-right': '0.3em'});
    error.append(message);

    var label_id = jQuery(element).attr('id').split('_')[1];
    var label = jQuery('label[for=' + label_id + ']');
    if(label.length){
      var strong = jQuery('<strong>');
      strong.text(label.text() + ': ');
      error.append(strong);
    }
    error.append(msg);
    error.append('<div style="clear: both" />');
  },

  clear: function(form){
    jQuery('.ui-state-error').removeClass('ui-state-error');
    jQuery('.submitting').removeClass('.submitting');
    jQuery('#form-validator-errors').remove();
  }
};

FacetedEdit.FormSections = {
  initialize: function(){
    this.initialized = false;
    this.context = null;
    this.selected = null;

    var context = this;
    jQuery(FacetedEdit.Events).bind(FacetedEdit.Events.INITIALIZE_WIDGETS, function(){
      context.update();
    });
  },

  update: function(){
    if(!this.initialized){
      this.first_initialize();
      return;
    }
    jQuery('.faceted-section-header').remove();
    this.selected.removeClass('ui-tabs-selected');
    this.selected.click();
  },

  first_initialize: function(){
    var context = this;
    this.initialized = true;

    var column = jQuery('.faceted-column');
    if(!column.length){
      return;
    }

    column = jQuery(column[0]);
    var sections = jQuery('.faceted-section-header', column);
    if(!sections.length){
      return;
    }

    this.sections = sections.clone();
    jQuery('.faceted-section-header').remove();

    var div = jQuery('<div>');
    div.addClass('faceted-section-tabs');
    var ul = jQuery('<ul>').addClass('formTabs');

    this.sections.each(function(){
      var section = jQuery(this);
      var section_id = section.attr('id').split('---')[1];
      var li = jQuery('<li>');

      li.attr('id', 'section-tabs-' + section_id);
      li.attr('class', 'faceted-drag-drop formTab');
      li.click(function(){
        context.tab_clicked(this, section_id);
      });
      var a = jQuery('<a>');
      a.text(section.attr('title'));
      li.append(a);
      ul.append(li);
      if(!context.selected){
        context.selected = li;
      }
    });

    div.append(ul);
    jQuery('#faceted-edit-widgets-ajax').after(div);

    this.context = div;
    this.selected.click();

    // Make it droppable
    var tabs = jQuery('li', this.context);
    tabs.sortable({
      items: '.faceted-widget',
      connectWith: '.faceted-drag-drop',
      placeholder: 'ui-state-highlight',
      forcePlaceholderSize: false,
      opacity: 0.7,
      delay: 300,
      cursor: 'crosshair',
      tolerance: 'pointer',
      receive: function(evt, ui){
        var tab = jQuery(this);
        if(tab.hasClass('ui-tabs-selected')){
          jQuery(ui.sender).sortable('cancel');
          return;
        }
        context.receive_widget(ui.item, tab);
      }
    });
  },

  tab_clicked: function(tab, section_id){
    this.selected = jQuery(tab);
    if(this.selected.hasClass('ui-tabs-selected')){
      return false;
    }
    var tabs = jQuery('li', this.context);

    tabs.removeClass('ui-tabs-selected');
    this.selected.addClass('ui-tabs-selected');
    jQuery('a', tabs).removeClass('selected');
    jQuery('a', this.selected).addClass('selected');

    if(section_id == 'all'){
      jQuery('div.faceted-widgets').show();
      return false;
    }
    jQuery('div.faceted-widgets').hide();
    jQuery('div.faceted-' + section_id + '-widgets').show();
    return false;
  },

  receive_widget: function(widget, section){
    widget = jQuery(widget);
    section = jQuery(section);
    var context = this;
    widget.remove();
    var wid = widget.attr('id').split('_')[0];
    var sid = section.attr('id').replace('section-tabs-', '');
    context.selected = section;

    // Submit
    var action = FacetedEdit.BASEURL + '@@faceted_configure';
    var query = {
      redirect:'',
      updateCriterion_button:'Save',
      cid: wid
    };
    query[wid + '_section'] = sid;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(action, query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.RELOAD_WIDGETS, {msg: data});
    });
  }
};

FacetedEdit.Catalog = {
  initialize: function(){
    this.types = {};
    var context = this;
    jQuery.getJSON(FacetedEdit.BASEURL + '@@faceted.catalog.types.json', {}, function(data){
      context.types = data;
    });

    jQuery(FacetedEdit.Events).bind(FacetedEdit.Events.CATALOG_CHANGED, function(evt, data){
      context.handle_change(data.catalog, data.operator);
    });
  },

  get: function(key){
    return this.types[key];
  },

  handle_change: function(catalog, operator){
    var select = jQuery('#archetypes-fieldname-operator select');
    var index = catalog.val();
    var mapping = this.get(index);
    var values = mapping ? mapping.operator : ['or'];

    select.empty();
    jQuery('option', operator).each(function(){
      var option = jQuery(this).attr('value');
      if(jQuery.inArray(option, values) != -1){
        select.append(jQuery(this).clone());
      }
    });
  }
};

FacetedEdit.FormPage = {
  initialize: function(){
    this.cookie_id = 'faceted-config-disable-ajax';
    var use_ajax = true;
    if(jQuery.cookie){
      if(jQuery.cookie(this.cookie_id)){
        use_ajax = false;
      }
      if(use_ajax){
        this.add_ajax_button('Disable AJAX', 'configure_faceted.html', 'disable');
      }else{
        this.add_ajax_button('Enable AJAX', 'configure_faceted.html', null);
      }
    }

    if(use_ajax){
      FacetedEdit.FormAddWidgets.initialize();
      FacetedEdit.FormImportExport.initialize();
      FacetedEdit.FormWidgets.initialize();
      FacetedEdit.FormMessage.initialize();
      FacetedEdit.FormPosition.initialize();
      FacetedEdit.FormEditWidget.initialize();
      FacetedEdit.Window.initialize();
      FacetedEdit.FormSections.initialize();
      FacetedEdit.Catalog.initialize();
    }else{
      jQuery('#faceted-edit-select-all-items').css('display', 'inline');
    }
  },

  add_ajax_button: function(label, action, cookie){
    var button = jQuery('<span>');
    var context = this;
    button.html('X');
    if(cookie){
      button.attr('class', 'ui-icon ui-icon-extlink');
    }else{
      button.attr('class', 'ui-icon ui-icon-newwin');
    }
    button.attr('title', label);
    button.css('cursor', 'pointer');
    button.click(function(){
      jQuery.cookie(context.cookie_id, cookie);
      window.location.href = action;
    });
    jQuery('#faceted-page-title').after(button);
  }
};

FacetedEdit.Load = function(evt, baseurl){
  if(baseurl){
    FacetedEdit.BASEURL = baseurl;
  }

  FacetedEdit.FormPage.initialize();
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

      var widget = FacetedEdit.Widgets[wid];
      widget.set_default();
      return false;
    };
  }
};

FacetedEdit.Unload = function(){
};
