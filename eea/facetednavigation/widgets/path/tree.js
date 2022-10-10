var FacetedTree = (window.FacetedTree = { version: "15.0" });

FacetedTree.Events = {};
FacetedTree.Events.CHANGED = "FACETEDTREE-CHANGED";
FacetedTree.Events.AJAX_START = "FACETEDTREE-AJAX-START";
FacetedTree.Events.AJAX_STOP = "FACETEDTREE-AJAX-STOP";

FacetedTree.JsTree = function (wid, container, mode) {
    var self = this;
    self.BASEURL = "";
    if (window.FacetedEdit) {
        self.BASEURL = FacetedEdit.BASEURL;
    } else if (window.Faceted) {
        self.BASEURL = Faceted.BASEURL;
    }
    self.wid = wid;
    self.mode = mode || "view";
    self.input = jQuery(container).find(`#${wid}`);
    self.input.attr("readonly", "readonly");

    self.area = jQuery("<div>")
        .attr("id", `${wid}-tree`)
        .addClass("tree")
        .text("Loading...")
        .width(self.input.width())
        .hide();
    self.input.after(self.area);

    self.input.on("click", function () {
        self.show();
    });

    jQuery(document).on("click", function (e) {
        var target = jQuery(e.target);
        if (target.is(`#${self.input.attr("id")}`)) {
            return;
        }
        var parent = target.parents(`#${self.area.attr("id")}`);
        if (parent.length) {
            return;
        }
        self.hide();
    });

    jQuery(document).on("keydown", function (e) {
        if (e.keyCode == 27) {
            self.hide();
        }
    });

    self.initialize();
};

FacetedTree.JsTree.prototype = {
    initialize: function () {
        var self = this;
        self.area
            .jstree({
                plugins: ["wholerow"],
                core: {
                    themes: {
                        name: "proton",
                        responsive: true,
                        variant: "large",
                    },
                    data: {
                        url: function (node) {
                            if (node.id === "#") {
                                return `${self.BASEURL}@@faceted.path.tree.json?cid=${self.wid}&mode=${self.mode}`;
                            }
                            return `${self.BASEURL}@@faceted.path.tree.json?cid=${self.wid}&mode=${self.mode}&path=${node.data.path}`;
                        },
                        dataType: "json",
                    },
                },
            })
            .on("changed.jstree", function (e, data) {
                self.change(data.node);
            });
    },

    show: function () {
        this.area.show();
    },

    hide: function () {
        this.area.hide();
    },

    change: function (node) {
        this.hide();
        var value = node.data.path;
        if (this.input.val() == value) {
            value = "";
        }
        this.input.val(value);
        jQuery(FacetedTree.Events).trigger(FacetedTree.Events.CHANGED, { path: value });
    },
};
