FacetedEdit.ETagWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");
    this.input = jQuery("#" + this.wid);
    this.selected = this.input;

    jQuery("form", this.widget).on("submit", function () {
        return false;
    });

    var js_widget = this;
    this.input.on("change", function () {
        js_widget.set_default(this);
    });
};

FacetedEdit.ETagWidget.prototype = {
    set_default: function () {
        this.selected = this.input;
        var value = this.selected.val();

        var query = {};
        query.redirect = "";
        query.updateCriterion_button = "Save";
        query.cid = this.wid;
        query["faceted." + query.cid + ".default"] = value;

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

FacetedEdit.initializeETagWidget = function () {
    jQuery("div.faceted-etag-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        FacetedEdit.Widgets[wid] = new FacetedEdit.ETagWidget(wid);
    });
};

// Initialize
jQuery(FacetedEdit.Events).on(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeETagWidget
);
