FacetedEdit.DateWidget = function (wid) {
    var self = this;
    self.wid = wid;
    self.widget = jQuery("#" + wid + "_widget");

    self.select_from = jQuery("select[name=from]", this.widget);
    self.select_to = jQuery("select[name=to]", this.widget);

    // Bind events
    self.select_from.on("change", function () {
        self.set_default(self.select_from, self.select_to);
    });

    self.select_to.on("change", function () {
        self.set_default(self.select_from, self.select_to);
    });

    this.selected = [];
};

FacetedEdit.DateWidget.prototype = {
    set_default: function (from, to) {
        var from_val = from.val();
        var to_val = to.val();
        var value = "";
        if (from_val === "now-past" && to_val === "now_future") {
            value = "";
        } else {
            value = from_val + "=>" + to_val;
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

FacetedEdit.initializeDateWidget = function () {
    jQuery("div.faceted-date-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        FacetedEdit.Widgets[wid] = new FacetedEdit.DateWidget(wid);
    });
};

jQuery(document).ready(function () {
    jQuery(FacetedEdit.Events).bind(
        FacetedEdit.Events.INITIALIZE_WIDGETS,
        FacetedEdit.initializeDateWidget
    );
});
