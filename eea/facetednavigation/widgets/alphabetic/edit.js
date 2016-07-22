FacetedEdit.AlphabeticalWidget = function(wid){
  this.wid = wid;
  this.widget = jQuery('#' + wid + '_widget');
  this.letters = jQuery('span', this.widget);
  this.selected = jQuery('.faceted_letter_selected', this.widget);

  var js_widget = this;
  this.letters.click(function(){
    js_widget.letter_click(this);
  });
};

FacetedEdit.AlphabeticalWidget.prototype = {
  letter_click: function(letter, evt){
    this.set_default(letter);
  },

  letter_unselect: function(letter){
    jQuery(letter).removeClass('faceted_letter_selected');
    this.selected = [];
  },

  letter_select: function(letter){
    this.letter_unselect(this.letters);
    jQuery(letter).addClass('faceted_letter_selected');
    if(jQuery(letter).attr('id').split('-')[1] != 'all'){
      this.selected = [letter];
    }
  },

  set_default: function(letter){
    var query = {};
    query.redirect = '';
    query.updateCriterion_button = 'Save';
    query.cid = this.wid;

    var value = jQuery(letter).attr('id').split('-')[1];
    var selected_value = '';
    if(this.selected.length){
      selected_value = jQuery(this.selected[0]).attr('id').split('-')[1];
    }
    if(value == selected_value){
      this.letter_select(jQuery('#' + this.wid + '-all'), this.widget);
      value = '';
    }else{
      this.letter_select(letter);
    }

    if(value == "all"){
      value = "";
    }

    query['faceted.' + this.wid + '.default'] = value;

    jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {msg: 'Saving ...'});
    jQuery.post(FacetedEdit.BASEURL + '@@faceted_configure', query, function(data){
      jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {msg: data});
    });

    return false;
  }
};

FacetedEdit.initializeAlphabeticalWidget = function(){
  jQuery('div.faceted-alphabetic-widget').each(function(){
      var wid = jQuery(this).attr('id');
      wid = wid.split('_')[0];
      FacetedEdit.Widgets[wid] = new FacetedEdit.AlphabeticalWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeAlphabeticalWidget);
});
