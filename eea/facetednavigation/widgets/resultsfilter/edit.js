FacetedEdit.ResultsFilterWidget = function (wid) {
    var self = this;
    self.wid = wid;
    self.widget = jQuery("#" + wid + "_widget");
    self.form = jQuery("form", self.widget);
    self.input = jQuery("#" + self.wid);
    self.selected = self.input;

    self.form.on("submit", function () {
        self.set_default(self.input);
        return false;
    });

    self.input.on("change", function () {
        self.set_default(this);
    });
};

FacetedEdit.ResultsFilterWidget.prototype = {
    set_default: function () {
        var self = this;
        self.selected = self.input;
        var value = self.selected.val();

        var query = {};
        query.redirect = "";
        query.updateCriterion_button = "Save";
        query.cid = self.wid;
        query["faceted." + self.wid + ".default"] = value;

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

FacetedEdit.initializeResultsFilterWidget = function () {
    jQuery("div.faceted-resultsfilter-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        FacetedEdit.Widgets[wid] = new FacetedEdit.ResultsFilterWidget(wid);
    });
};

// Initialize
jQuery(FacetedEdit.Events).on(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeResultsFilterWidget
);
