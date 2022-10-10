/* Path Widget
 */
Faceted.PathWidget = function (wid) {
    var self = this;
    self.wid = wid;
    self.widget = jQuery(`#${wid}_widget`);
    self.widget.show();
    self.title = jQuery("legend", self.widget).html();
    self.input = jQuery("input", self.widget);
    self.breadcrumbs = jQuery("<dd>");
    self.selected = [];

    // Default value
    var value = self.input.val();
    if (value) {
        self.selected = self.input;
        Faceted.Query[self.wid] = [value];
    }

    // Navigation Tree
    self.tree = new FacetedTree.JsTree(self.wid, self.widget);

    // Bind events
    jQuery("form", self.widget).on("submit", function () {
        return false;
    });
    jQuery(FacetedTree.Events).on(FacetedTree.Events.CHANGED, function () {
        self.text_change(self.input);
    });
    jQuery(Faceted.Events).on(Faceted.Events.QUERY_CHANGED, function () {
        self.synchronize();
    });
    jQuery(Faceted.Events).on(Faceted.Events.RESET, function () {
        self.reset();
    });
};

Faceted.PathWidget.prototype = {
    text_change: function (element) {
        this.do_query(element);
    },

    do_query: function (element) {
        var value = this.input.val();
        value = value ? [value] : [];

        if (!element) {
            this.selected = [];
            return Faceted.Form.do_query(this.wid, []);
        }
        this.selected = [this.input];
        return Faceted.Form.do_query(this.wid, value);
    },

    reset: function () {
        this.selected = [];
        this.widget.removeClass("faceted-widget-active");
        this.input.val("");
    },

    synchronize: function () {
        var value = Faceted.Query[this.wid];
        if (!value) {
            this.reset();
            return;
        }
        this.input.val(value);
        this.selected = [this.input];
        this.widget.addClass("faceted-widget-active");
    },

    criteria: function () {
        var html = [];
        var title = this.criteria_title();
        var body = this.criteria_body();
        if (title) {
            html.push(title);
        }
        if (body) {
            html.push(body);
        }
        return html;
    },

    criteria_title: function () {
        if (!this.selected.length) {
            return "";
        }
        var link = jQuery('<a href="#" class="faceted-remove">remove</a>');
        link.attr("id", `criteria_${this.wid}`);
        link.attr("title", `Remove ${this.title} filters`);
        var widget = this;
        link.on("click", function () {
            widget.criteria_remove();
            return false;
        });

        var html = jQuery("<dt>");
        html.attr("id", `criteria_${this.wid}_label`);
        html.append(link);
        html.append(`<span>${this.title}</span>`);
        return html;
    },

    criteria_body: function () {
        if (!this.selected.length) {
            return "";
        }

        var self = this;
        self.breadcrumbs.text("Loading...");
        var query = {};
        query.path = self.input.val();
        query.cid = self.wid;
        jQuery.getJSON(
            `${Faceted.BASEURL}@@faceted.path.breadcrumbs.json`,
            query,
            function (data) {
                self.breadcrumbs.empty();
                jQuery.each(data, function () {
                    self.breadcrumbs.append(jQuery("<span>").html("&raquo;"));
                    var a = jQuery("<a>")
                        .attr("href", this.url)
                        .attr("title", this.title)
                        .text(this.title)
                        .on("click", function () {
                            var path = jQuery(this).attr("href");
                            self.input.val(path);
                            jQuery(FacetedTree.Events).trigger(
                                FacetedTree.Events.CHANGED,
                                { path: path }
                            );
                            return false;
                        });
                    self.breadcrumbs.append(a);
                });
            }
        );
        return self.breadcrumbs;
    },

    criteria_remove: function () {
        this.selected = [];
        this.input.val("");
        this.do_query();
    },
};

Faceted.initializePathWidget = function () {
    jQuery("div.faceted-path-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.PathWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializePathWidget);
