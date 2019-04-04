FacetedEdit.MultiSelectWidget = function(wid){
  var self = this;
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.title = this.widget.find('legend').html();
  this.elements = jQuery('option', this.widget);
  this.select = jQuery('#' + this.wid);
  this.multiple = this.select.attr("multiple") ? true : false;
  this.placeholder = this.widget.data('placeholder');

  this.select.select2({
    placeholder: this.placeholder,
    allowClear: true
  });

  self.operatorValue = self.widget.data('operator');

  self.operator = self.widget.find('.faceted-operator a');
  if(self.operator.length){
    self.operatorValue = self.operator.data('value');
    self.operator.text( self.operator.data( self.operatorValue ) );

    self.operator.click(function(evt){
      evt.preventDefault();

      if(self.operatorValue === 'or'){
        self.operatorValue = 'and';
        self.operator.text(self.operator.data('and'));
      }else{
        self.operatorValue = 'or';
        self.operator.text(self.operator.data('or'));
      }

      self.set_default(this);
    });
  }

  // Handle change
  var js_widget = this;
  this.select.change(function(evt){
    js_widget.set_default(this);
  });

  this.count();
};

FacetedEdit.MultiSelectWidget.prototype = {
  count: function(){
    if(!this.widget.hasClass('faceted-count')){
      return;
    }
    this.elements.each(function(){
      var option = jQuery(this);
      var number = Math.floor(Math.random() * 100);
      var option_txt = option.attr('title');
      option_txt += ' (' + number + ')';
      option.html(option_txt);
    });
  },

  set_default: function(element){
    var value = "";
    if(this.multiple){
      jQuery(this.select.val()).each(function(idx, val){
        if(idx > 0){
          value += "\n";
        }
        value += val;
      });
    } else {
      value = this.select.val();
    }

    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;
    query['faceted.' + this.wid + '.default'] = value;
    query['faceted.' + this.wid + '.operator'] = this.operatorValue;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });
  }
};

FacetedEdit.initializeMultiSelectWidget = function(){
  jQuery('div.faceted-multiselect-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.MultiSelectWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeMultiSelectWidget);
});
