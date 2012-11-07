FacetedEdit.CheckboxesWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.fieldset = jQuery('.widget-fieldset', this.widget);
  this.elements = jQuery('input[type=checkbox]', this.widget);
  this.selected = jQuery('input[type=checkbox]:checked', this.widget);
  this.maxitems = parseInt(jQuery('span', this.widget).text(), 10);
  if(this.maxitems){
    this.fieldset.collapsible({
      maxitems: this.maxitems
    });
  }

  var js_widget = this;
  this.elements.click(function(evt){
    js_widget.set_default(this);
  });
  this.count();
};

FacetedEdit.CheckboxesWidget.prototype = {
  count: function(){
    if(!this.widget.hasClass('faceted-count')){
      return;
    }
    jQuery('li', this.widget).each(function(){
      var li = jQuery(this);
      var number = Math.floor(Math.random() * 100);
      var span = jQuery('span', li);
      if(!span.length){
        li.append(jQuery('<span>'));
        span = jQuery('span', li);
      }
      span.text('(' + number + ')');
    });
  },

  set_default: function(element){
    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;

    this.selected = jQuery('#' + this.wid + '_widget input[type=checkbox]:checked');
    var value = [];
    this.selected.each(function(){
      value.push(jQuery(this).val());
    });
    query[this.wid + '_default'] = value.length ? value : '';

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeCheckboxesWidget = function(){
  jQuery('div.faceted-checkboxes-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.CheckboxesWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeCheckboxesWidget);
});
