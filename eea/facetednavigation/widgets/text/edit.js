FacetedEdit.TextWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");
    this.button = jQuery("input[type=submit]", this.widget);
    this.input = jQuery("#" + this.wid);
    this.selected = this.input;

    var js_widget = this;
    this.button.on("click", function () {
        js_widget.set_default(this);
    });

    this.input.on("change", function () {
        js_widget.set_default(this);
    });
};

FacetedEdit.TextWidget.prototype = {
    set_default: function () {
        this.selected = this.input;
        var value = this.selected.val();

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

FacetedEdit.initializeTextWidget = function () {
    jQuery("div.faceted-text-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        FacetedEdit.Widgets[wid] = new FacetedEdit.TextWidget(wid);
    });
};

// Initialize
jQuery(FacetedEdit.Events).on(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeTextWidget
);
