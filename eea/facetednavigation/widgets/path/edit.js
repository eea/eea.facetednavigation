FacetedEdit.PathWidget = function (wid) {
    var self = this;
    self.wid = wid;
    self.widget = jQuery(`#${wid}_widget`);
    self.tree = new FacetedTree.JsTree(self.wid, self.widget, "edit");
    self.initialize();
};

FacetedEdit.PathWidget.prototype = {
    initialize: function () {
        var self = this;
        self.form = self.widget.find("form");
        self.input = self.widget.find("input");
        self.selected = self.input;

        self.form.on("submit", function () {
            self.set_default(self.input);
            return false;
        });

        // Navigation Tree
        jQuery(FacetedTree.Events).on(FacetedTree.Events.CHANGED, function () {
            self.set_default(self.input);
        });
    },

    set_default: function (element) {
        var self = this;
        self.selected = element;
        var value = self.selected.val();

        var query = {
            redirect: "",
            updateCriterion_button: "Save",
            cid: self.wid,
            [`faceted.${self.wid}.default`]: value,
        };

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

FacetedEdit.initializePathWidget = function () {
    jQuery("div.faceted-path-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        FacetedEdit.Widgets[wid] = new FacetedEdit.PathWidget(wid);
    });
};

jQuery(function () {
    jQuery(FacetedEdit.Events).on(
        FacetedEdit.Events.INITIALIZE_WIDGETS,
        FacetedEdit.initializePathWidget
    );
});
