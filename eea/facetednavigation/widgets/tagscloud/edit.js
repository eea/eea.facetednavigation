FacetedEdit.TagsCloudWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.type = 'tagscloud';
  this.tags = jQuery('li', this.widget);
  this.selected = jQuery('.faceted-tag-selected', this.widget);
  this.config = {};
  this.initialize();

  var js_widget = this;
  this.tags.click(function(){
    js_widget.tag_click(this);
  });
};

FacetedEdit.TagsCloudWidget.prototype = {
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

    this.count();
    this.update();
  },

  update: function(){
    jQuery('#' + this.wid, this.widget).tagcloud(this.config);
  },

  count: function(){
    if(!this.widget.hasClass('faceted-count')){
      return;
    }

    this.tags.each(function(){
      var tag = jQuery(this);
      var html = tag.text();
      html = html.replace(/\s\(\d+\)/, '');
      html += ' (' + tag.attr('value') + ')';
      tag.html(html);
    });
  },

  tag_click: function(tag){
    this.set_default(tag);
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

  set_default: function(tag){
    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;

    var value = jQuery(tag).attr('id').replace(this.wid, '');
    value = value.replace(/_-_/g, ' ');
    var selected_value = '';
    if(this.selected.length){
      selected_value = jQuery(this.selected[0]).attr('id').replace(this.wid, '');
      selected_value = selected_value.replace(/_-_/g, ' ');
    }
    if(value == selected_value){
      this.select(jQuery('#' + this.wid + 'all', this.widget));
      value = '';
    }else{
      this.select(tag);
    }

    if(value == 'all'){
      value = '';
    }
    query['faceted.' + this.wid + '.default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeTagsCloudWidget = function(){
  jQuery('div.faceted-tagscloud-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.TagsCloudWidget(wid);
  });
};

FacetedEdit.resizeTagsCloudWidgets = function(){
  jQuery.each(FacetedEdit.Widgets, function(wid){
    var js_widget = FacetedEdit.Widgets[wid];
    if(js_widget.type != 'tagscloud'){
      return;
    }
    var width = js_widget.widget.width();
    jQuery('ul', js_widget.widget).width(width - 30);
    js_widget.update();
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeTagsCloudWidget);

  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.POSITION_UPDATED,
    FacetedEdit.resizeTagsCloudWidgets);

  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.WINDOW_WIDTH_CHANGED,
    FacetedEdit.resizeTagsCloudWidgets);
});
