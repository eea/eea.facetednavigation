var FacetedTree = {version: '1.0.0'};

FacetedTree.Events = {};
FacetedTree.Events.CHANGED = 'FACETEDTREE-CHANGED'

FacetedTree.JsTree = function(wid, container){
  this.wid = wid;
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
  this.area.tree({
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
        draggable  : false,
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

  jQuery(document).keydown(function(e){
    if(e.keyCode == 27){
      js_tree.hide();
    }
  });
};

FacetedTree.JsTree.prototype = {
  show: function(){
    var js_tree = this;
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
