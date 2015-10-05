Faceted.TagsCloudWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.widget.show();
  this.title = jQuery('legend', this.widget).html();
  this.tags = jQuery('li', this.widget);
  this.faceted_count = this.widget.hasClass('faceted-count');
  this.selected = [];

  // Faceted version
  this.version = '';
  var version = jQuery('#faceted-version');
  if(version){
    this.version = version.text();
  }

  this.config = {};
  this.initialize();

  var selected = jQuery('.faceted-tag-selected', this.widget);
  if(selected.length){
    var value = selected.attr('id').replace(this.wid, '');
    value = value.replace(/_-_/g, ' ');
    Faceted.Query[this.wid] = [value];
    this.synchronize();
  }

  // Handle clicks
  var js_widget = this;
  this.tags.click(function(evt){
   js_widget.tag_click(this, evt);
  });

  // Bind events
  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
    js_widget.synchronize();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.RESET, function(evt){
    js_widget.reset();
  });

  jQuery(Faceted.Events).bind(Faceted.Events.QUERY_INITIALIZED, function(evt){
    js_widget.count();
  });
  jQuery(Faceted.Events).bind(Faceted.Events.FORM_DO_QUERY, function(evt, data){
    if(data.wid == js_widget.wid || data.wid == 'b_start'){
      return;
    }
    js_widget.count();
  });

  // Resize window
  jQuery(Faceted.Events).bind(Faceted.Events.WINDOW_WIDTH_CHANGED, function(evt, data){
    var width = js_widget.widget.width();
    jQuery('ul', js_widget.widget).width(width - 30);
    js_widget.update();
  });
};

Faceted.TagsCloudWidget.prototype = {
  initialize: function(){
    var cloud = jQuery('#' + this.wid + '-cloud', this.widget).text();
    cloud = cloud ? cloud : 'list';
    var sizemin = jQuery('#' + this.wid + '-sizemin', this.widget).text();
    sizemin = parseInt(sizemin, 10);
    sizemin = sizemin ? sizemin : 10;
    var sizemax = jQuery('#' + this.wid + '-sizemax', this.widget).text();
    sizemax = parseInt(sizemax, 10);
    sizemax = sizemax ? sizemax : 20;
    var colormin = jQuery('#' + this.wid + '-colormin', this.widget).text();
    var colormax = jQuery('#' + this.wid + '-colormax', this.widget).text();
    var height = jQuery('#' + this.wid + '-height', this.widget).text();
    height = parseInt(height, 10);
    height = height ? height : 200;
    height = (cloud == 'list') ? 'auto' : height;
    this.config = {
      type: cloud,
      sizemin: sizemin,
      sizemax: sizemax,
      height: height,
      colormin: colormin,
      colormax: colormax
    };
    this.update();
  },

  update: function(){
    jQuery('#' + this.wid, this.widget).tagcloud(this.config);
  },

  tag_click: function(tag, evt){
    this.do_query(tag);
  },

  unselect: function(tag){
    jQuery(tag).removeClass('faceted-tag-selected');
    this.selected = [];
  },

  select: function(tag){
    this.unselect(this.tags);
    jQuery(tag).addClass('faceted-tag-selected');
    if(jQuery(tag).attr('id').replace(this.wid, '') != 'all'){
      this.selected = [tag];
    }
  },

  do_query: function(tag){
    var value=jQuery(tag).attr('id').replace(this.wid, '');
    value = value.replace(/_-_/g, ' ');
    var selected_value = '';
    if(this.selected.length){
      selected_value = jQuery(this.selected[0]).attr('id').replace(this.wid, '');
      selected_value = selected_value.replace(/_-_/g, ' ');
    }
    if(value == selected_value){
      this.select(jQuery('#' + this.wid + 'all', this.widget));
      value = [];
    }else{
      this.select(tag);
    }
    Faceted.Form.do_query(this.wid, value);
  },

  reset: function(){
    this.select(jQuery('#' + this.wid + 'all', this.widget));
  },

  synchronize: function(){
    var value = Faceted.Query[this.wid];
    if(!value){
      this.reset();
    }else{
      value = value[0].replace(/ /g, '_-_');
      var tag = jQuery('#' + this.wid + value, this.widget);
      if(tag.length){
        this.select(tag[0]);
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
    var tag_id = jQuery(this.selected[0]).attr('id');
    var label = jQuery(this.selected[0]).attr('title');
    var link = jQuery('<a href="#">[X]</a>');
    link.attr('id', 'criteria_' + tag_id);
    link.attr('title', 'Remove ' + label + ' filter');

    var widget = this;
    link.click(function(evt){
      widget.criteria_remove(this, evt);
      return false;
    });

    var html = jQuery('<dd>');
    var span = jQuery('<span class="faceted-tagscloud-criterion">');
    html.attr('id', 'criteria_' + this.wid + '_entries');

    span.append(link);
    jQuery('<span>').text(label).appendTo(span);
    html.append(span);
    return html;
  },

  criteria_remove: function(tag, evt){
    this.do_query(this.selected[0]);
  },

  count: function(){
    var query = Faceted.SortedQuery();
    query.cid = this.wid;
    if(this.version){
      query.version = this.version;
    }
    var context = this;

    jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_START, {wid: context.wid});
    jQuery.get(Faceted.BASEURL + '@@tagscloud_counter', query, function(data){
      context.count_update(data);
      jQuery(Faceted.Events).trigger(Faceted.Events.DO_UPDATE);
      jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_STOP, {wid: context.wid});
    });
  },

  count_update: function(data){
    var js_widget = this;
    var all_id = js_widget.wid + 'all';
    var fieldset = jQuery('fieldset', jQuery(data));
    js_widget.widget.html(fieldset);

    var min = 10000;
    jQuery('li', js_widget.widget).each(function(){
      var tag = jQuery(this);
      var val = tag.attr('value');
      val = parseInt(val, 10);
      if(val < min && val > 0){
        min = val;
      }
    });
    var all_tag = jQuery('#' + all_id, js_widget.widget);
    var all = all_tag.attr('value');
    all_tag.attr('value', min);

    js_widget.tags = jQuery('li', this.widget);

    // Handle clicks
    js_widget.tags.click(function(evt){
     js_widget.tag_click(this, evt);
    });

    if(!js_widget.faceted_count){
      // Update
      js_widget.update();
      return;
    }

    // Count
    js_widget.tags.each(function(){
      var tag = jQuery(this);

      var html = tag.text();
      var value = parseInt(tag.attr('value'), 10);

      if(tag.attr('id') == all_id){
        value = all;
      }else{
        value -= 1;
      }

      html = html.replace(/\s\(\d+\)/, '');
      html += ' (' + value + ')';
      tag.html(html);

      tag.unbind();
      if((tag.attr('value')===1) && (tag.attr('id') != all_id)){
        tag.addClass('faceted-tag-disabled');
      }else{
        tag.removeClass('faceted-tag-disabled');
        tag.click(function(evt){
          js_widget.tag_click(this, evt);
        });
      }
    });

    // Update
    js_widget.update();
  }
};

Faceted.initializeTagsCloudWidget = function(evt){
  jQuery('div.faceted-tagscloud-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.TagsCloudWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeTagsCloudWidget);
});
