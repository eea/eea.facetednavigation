/* Select Widget
 */
Faceted.SelectWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + this.wid + "_widget");
    this.widget.show();
    this.title = this.widget.find("legend").html();
    this.elements = this.widget.find("option");
    this.select = jQuery("#" + this.wid);
    this.selected = [];

    // Faceted version
    this.version = "";
    var version = jQuery("#faceted-version");
    if (version) {
        this.version = version.text();
    }

    // Handle change
    jQuery("form", this.widget).on("submit", function () {
        return false;
    });

    var js_widget = this;
    this.select.on("change", function (evt) {
        js_widget.select_change(this, evt);
    });

    // Default value
    var value = this.select.val();
    if (value) {
        this.selected = js_widget.widget.find("option:selected");
        Faceted.Query[this.wid] = [value];
    }

    // Bind events
    jQuery(Faceted.Events).on(Faceted.Events.QUERY_CHANGED, function () {
        js_widget.synchronize();
    });
    jQuery(Faceted.Events).on(Faceted.Events.RESET, function () {
        js_widget.reset();
    });
    if (this.widget.hasClass("faceted-count")) {
        var sortcountable = this.widget.hasClass("faceted-sortcountable");
        jQuery(Faceted.Events).on(Faceted.Events.QUERY_INITIALIZED, function () {
            js_widget.count(sortcountable);
        });
        jQuery(Faceted.Events).on(Faceted.Events.FORM_DO_QUERY, function (evt, data) {
            if (data.wid == js_widget.wid || data.wid == "b_start") {
                return;
            }
            js_widget.count(sortcountable);
        });
    }
};

Faceted.SelectWidget.prototype = {
    select_change: function (element) {
        if (!jQuery(element).val()) {
            element = null;
        }
        this.do_query(element);
    },

    do_query: function (element) {
        if (!element) {
            this.selected = [];
            return Faceted.Form.do_query(this.wid, []);
        } else {
            var value = jQuery(element).val();
            this.selected = this.widget.find("option:selected");
            return Faceted.Form.do_query(this.wid, value);
        }
    },

    reset: function () {
        if (this.widget.hasClass("hide-all-option")) {
            var first_val = this.select.find("option:first").val();
            this.select.val(first_val);
            this.selected = [first_val];
            this.select_change(this.select);
        } else {
            this.select.val("");
            this.selected = [];
        }
        this.widget.removeClass("faceted-widget-active");
    },

    synchronize: function () {
        var value = Faceted.Query[this.wid];
        if (!value) {
            this.reset();
            return;
        }

        var context = this;
        jQuery.each(value, function () {
            var selected = context.widget.find('option[value="' + this + '"]');
            if (!selected.length) {
                context.reset();
            } else {
                context.selected = selected;
                context.select.val(value);
                context.widget.addClass("faceted-widget-active");
            }
        });
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

        var widget = this;
        var html = jQuery("<dd>");
        var span = jQuery('<span class="faceted-select-criterion">');
        html.attr("id", "criteria_" + this.wid + "_entries");
        var element = jQuery(this.selected);
        var value = element.val();
        var label = element.attr("title");
        var link = jQuery('<a href="#" class="faceted-remove">remove</a>');

        link.attr("id", "criteria_" + this.wid + "_" + value);
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
        this.select.val("");
        this.do_query();
    },

    count: function (sortcountable) {
        var query = Faceted.SortedQuery();
        query.cid = this.wid;
        if (this.version) {
            query.version = this.version;
        }

        var context = this;
        jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_START, { wid: context.wid });
        jQuery.getJSON(Faceted.BASEURL + "@@faceted_counter", query, function (data) {
            context.count_update(data, sortcountable);
            jQuery(Faceted.Events).trigger(Faceted.Events.DO_UPDATE);
            jQuery(Faceted.Events).trigger(Faceted.Events.AJAX_STOP, {
                wid: context.wid,
            });
        });
    },

    count_update: function (data, sortcountable) {
        var context = this;
        var select = jQuery("select", context.widget);
        var options = jQuery("option", context.widget);
        var current_val = select.val();
        jQuery(options).each(function () {
            var option = jQuery(this);
            option.removeClass("faceted-select-item-disabled");
            option.attr("disabled", false);
            var key = option.val();

            var value = data[key];
            value = value ? value : 0;
            var option_txt = option.attr("title");
            option_txt += " (" + value + ")";

            option.html(option_txt);
            if (sortcountable) {
                option.data("count", value);
            }
            if (!value) {
                option.attr("disabled", "disabled");
                option.addClass("faceted-select-item-disabled");
            }
        });
        if (sortcountable) {
            options.detach().sort(function (x, y) {
                var a = jQuery(x).data("count");
                var b = jQuery(y).data("count");
                return b - a;
            });
            select.append(options);
            select.val(current_val);
        }
    },
};

Faceted.initializeSelectWidget = function () {
    jQuery("div.faceted-select-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.SelectWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializeSelectWidget);
