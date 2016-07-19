FacetedEdit.CheckboxesWidget = function(wid){
  var self = this;
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.fieldset = jQuery('.widget-fieldset', this.widget);
  this.elements = jQuery('input[type=checkbox]', this.widget);
  this.selected = jQuery('form input[type=checkbox]:checked', this.widget);
  this.boolean = this.widget.hasClass('faceted-boolean-widget');

  this.maxitems = parseInt(jQuery('span', this.widget).text(), 10);
  if(this.maxitems){
    this.fieldset.collapsible({
      maxitems: this.maxitems
    });
  }

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

    this.selected = this.widget.find('input[type=checkbox]:checked');

    var value = "";
    this.selected.each(function(idx){
      if(idx > 0){
        value += "\n";
      }
      value += jQuery(this).val();
    });

    if(this.boolean){
      if(!value) {
        query['faceted.' + this.wid + '.default-empty-marker'] = 1;
      } else {
        query['faceted.' + this.wid + '.default'] = value;
      }
    } else {
      query['faceted.' + this.wid + '.default'] = value;
      query['faceted.' + this.wid + '.operator'] = this.operatorValue;
    }

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
