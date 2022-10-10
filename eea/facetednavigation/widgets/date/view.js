/* Relative Date Widget
 */
Faceted.DateWidget = function (wid) {
    var self = this;
    self.wid = wid;
    self.widget = jQuery("#" + wid + "_widget");
    self.widget.show();
    self.title = jQuery("legend", self.widget).html();
    self.select_from = jQuery("select[name=from]", self.widget);
    self.select_to = jQuery("select[name=to]", self.widget);

    self.selected = [];

    // Default value
    var from = self.select_from.val();
    var to = self.select_to.val();
    if (from !== "now-past" || to !== "now_future") {
        self.selected = [self.select_from, self.select_to];
        Faceted.Query[self.wid] = [from, to];
    }

    // Handle clicks
    jQuery("form", self.widget).on("submit", function () {
        return false;
    });

    // Bind events
    self.select_from.on("change", function () {
        self.change();
    });

    self.select_to.on("change", function () {
        self.change();
    });

    jQuery(Faceted.Events).on(Faceted.Events.QUERY_CHANGED, function () {
        self.synchronize();
    });
    jQuery(Faceted.Events).on(Faceted.Events.RESET, function () {
        self.reset();
    });
};

Faceted.DateWidget.prototype = {
    change: function () {
        var from = this.select_from.val();
        var to = this.select_to.val();
        if (from === "now-past" && to === "now_future") {
            this.reset();
            Faceted.Form.do_query(this.wid, []);
        } else {
            this.do_query();
        }
    },

    do_query: function () {
        this.sync_ui();
        var value = [this.select_from.val(), this.select_to.val()];
        this.selected = [this.select_from, this.select_to];
        Faceted.Form.do_query(this.wid, value);
    },

    reset: function () {
        this.selected = [];
        this.select_from.val("now-past");
        this.select_to.val("now_future");
        this.widget.removeClass("faceted-widget-active");
        this.sync_ui();
    },

    sync_ui: function () {
        this.select_from.find("option").attr("disabled", false);
        this.select_to.find("option").attr("disabled", false);

        var found;
        found = false;
        var from_value = this.select_from.val();
        this.select_to.find("option").each(function () {
            jQuery(this).attr("disabled", true);
            if (!found && this.value === from_value) {
                found = true;
                return false;
            }
        });

        found = false;
        var to_value = this.select_to.val();
        this.select_from.find("option").each(function () {
            if (this.value === to_value) {
                found = true;
            }
            if (found) {
                jQuery(this).attr("disabled", true);
            }
        });
    },

    synchronize: function () {
        var q_value = Faceted.Query[this.wid];
        if (!q_value) {
            this.reset();
            return;
        }
        if (!q_value.length) {
            this.reset();
            return;
        }
        if (q_value.length < 2) {
            this.reset();
            return;
        }

        this.select_from.val(q_value[0]).trigger("change");
        this.select_to.val(q_value[1]).trigger("change");
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
        link.attr("id", "criteria_" + this.wid);
        link.attr("title", "Remove " + this.title + " filters");
        var widget = this;
        link.on("click", function () {
            widget.criteria_remove();
            return false;
        });

        var html = jQuery("<dt>");
        html.attr("id", "criteria_" + this.wid + "_label");
        html.append(link);
        html.append("<span>" + this.title + "</span>");
        return html;
    },

    criteria_body: function () {
        if (!this.selected.length) {
            return "";
        }

        var from = jQuery("option:selected", this.select_from).text();
        var to = jQuery("option:selected", this.select_to).text();
        var label = from + " - " + to;

        var widget = this;
        var html = jQuery("<dd>");
        html.attr("id", "criteria_" + this.wid + "_entries");
        var span = jQuery('<span class="faceted-date-criterion">');
        var link = jQuery('<a href="#" class="faceted-remove">remove</a>');

        link.attr("id", "criteria_" + this.wid + "_");
        link.attr("title", "Remove " + label + " filter");
        link.on("click", function () {
            widget.criteria_remove();
            return false;
        });

        span.append(link);
        jQuery("<span>").text(label).appendTo(span);
        html.append(span);
        return html;
    },

    criteria_remove: function () {
        this.reset();
        return Faceted.Form.do_query(this.wid, []);
    },
};

Faceted.initializeDateWidget = function () {
    jQuery("div.faceted-date-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.DateWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializeDateWidget);
