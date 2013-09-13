var FacetedTree = {version: '2.0'};

FacetedTree.Events = {};
FacetedTree.Events.CHANGED = 'FACETEDTREE-CHANGED';
FacetedTree.Events.AJAX_START = 'FACETEDTREE-AJAX-START';
FacetedTree.Events.AJAX_STOP = 'FACETEDTREE-AJAX-STOP';

FacetedTree.JsTree = function(wid, container, mode){
  this.BASEURL = '';
  if(window.FacetedEdit){
    this.BASEURL = FacetedEdit.BASEURL;
  }else if(window.Faceted){
    this.BASEURL = Faceted.BASEURL;
  }
  this.wid = wid;
  this.mode = mode || 'view';
  this.input = jQuery('#' + wid, container);
  this.input.attr('readonly', 'readonly');
  this.theme = jQuery('#' + wid + '-theme', container);

  this.area = jQuery('<div>');
  this.area.addClass('tree');
  this.area.text('Loading...');
  this.area.hide();
  this.area.width(this.input.width());
  this.input.after(this.area);

  var js_tree = this;
  this.input.click(function(evt){
    js_tree.show();
  });

  jQuery(document).click(function(e){
    var target = jQuery(e.target);
    if(target.is('#' + js_tree.input.attr('id'))){
      return;
    }
    var parent = target.parents('#' + js_tree.area.attr('id'));
    if(parent.length){
      return;
    }
    js_tree.hide();
  });

  jQuery(document).keydown(function(e){
    if(e.keyCode == 27){
      js_tree.hide();
    }
  });

  var query = {};
  query.cid = this.wid;
  query.mode = this.mode;

  jQuery(FacetedTree.Events).trigger(FacetedTree.Events.AJAX_START, {msg: 'Loading ...'});
  jQuery.getJSON(js_tree.BASEURL + '@@faceted.path.tree.json', query, function(data){
    if(data.length){
      js_tree.initialize(data);
    }else{
      if(mode=='edit'){
        jQuery('form', container).hide();
        jQuery('div.faceted-path-errors', container).show();
      }else{
        jQuery('.faceted-widget:has(div.faceted-path-errors)').remove();
        jQuery(Faceted.Events).trigger(Faceted.Events.REDRAW);
      }
    }
    jQuery(FacetedTree.Events).trigger(FacetedTree.Events.AJAX_STOP, {msg: data});
  });
};

FacetedTree.JsTree.prototype = {
  initialize: function(static_tree){
    var js_tree = this;
    js_tree.area.tree({
      ui: {
        theme_name: js_tree.theme.attr('title'),
        theme_path: js_tree.theme.text()
      },

      types   : {
        "default" : {
          clickable  : true,
          renameable : false,
          deletable  : false,
          creatable  : false,
          draggable  : false
        }
      },

      data: {
        type: 'json',
        async: true,
        opts: {
          method: 'POST',
          url: js_tree.BASEURL  + '@@faceted.path.tree.json'
        }
      },
      callback: {
        beforedata: function(node, tree){
          if(node===false){
            tree.settings.data.opts['static'] = static_tree;
            return;
          }
          tree.settings.data.opts['static'] = false;
          var data = {cid: js_tree.wid};
          data.mode = js_tree.mode;
          if(node){
            data.path = node.attr('path');
          }
          return data;
        },
        onselect: function(node, tree){
          js_tree.change(node, tree);
        }
      }
    });
  },

  show: function(){
    this.area.show();
  },

  hide: function(){
    this.area.hide();
  },

  change: function(node, tree){
    this.hide();
    node = jQuery(node);
    var value = node.attr('path');
    if(this.input.val() == value){
      value = '';
    }
    this.input.val(value);
    jQuery(FacetedTree.Events).trigger(
      FacetedTree.Events.CHANGED, {path: value}
    );
  }
};
