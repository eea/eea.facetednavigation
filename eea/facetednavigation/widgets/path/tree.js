var FacetedTree = {version: '1.0.0'};

FacetedTree.Events = {};
FacetedTree.Events.CHANGED = 'FACETEDTREE-CHANGED'

FacetedTree.JsTree = function(wid, container){
  this.wid = wid;
  this.input = jQuery('#' + wid, container);
  this.input.attr('readonly', 'readonly');

  this.area = jQuery('<div>');
  this.area.addClass('tree');
  this.area.hide();
  this.area.width(this.input.width());
  //this.area.height(400);
  this.input.after(this.area);

  var js_tree = this;
  this.area.tree({
    ui: {
      theme_name: 'apple',
      theme_path: '/++resource++jquery.jstree/themes/apple/style.css'
    },

    types   : {
      "default" : {
        clickable       : true,
        renameable      : false,
        deletable       : false,
        creatable       : false,
        draggable       : false,
      }
    },

    data: {
      type: 'json',
      async: true,
      opts: {
        method: 'POST',
        url: '@@faceted.path.tree.json'
      }
    },
    callback: {
      beforedata: function(node, tree){
        var data = {cid: js_tree.wid};
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

  this.input.click(function(evt){
    js_tree.show();
  });
};

FacetedTree.JsTree.prototype = {
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
      return;
    }
    this.input.val(value);
    jQuery(FacetedTree.Events).trigger(FacetedTree.Events.CHANGED, {path: value})
  }
};
