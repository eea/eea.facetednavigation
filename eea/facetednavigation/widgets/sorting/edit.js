FacetedEdit.SortingWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");
    this.reverse = jQuery("#" + this.wid + "_reversed");
    this.elements = jQuery("option", this.widget);
    this.select = jQuery("#" + this.wid);
    this.value = this.select.val();

    // Handle select change
    var js_widget = this;
    this.select.on("change", function () {
        js_widget.set_default(this);
    });
    this.reverse.on("click", function () {
        js_widget.set_default(this);
    });
};

FacetedEdit.SortingWidget.prototype = {
    set_default: function () {
        var value = this.select.val();
        if (this.reverse.is(":checked")) {
            value += "(reverse)";
        }

        var query = {};
        query.redirect = "";
        query.updateCriterion_button = "Save";
        query.cid = this.wid;
        query["faceted." + this.wid + ".default"] = value;

        jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_START, {
            msg: "Saving ...",
        });
        jQuery.post(FacetedEdit.BASEURL + "@@faceted_configure", query, function (data) {
            jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {
                msg: data,
            });
        });
    },
};

FacetedEdit.initializeSortingWidget = function () {
    jQuery("div.faceted-sorting-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        FacetedEdit.Widgets[wid] = new FacetedEdit.SortingWidget(wid);
    });
};

// Initialize
jQuery(FacetedEdit.Events).on(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeSortingWidget
);
