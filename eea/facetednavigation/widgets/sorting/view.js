/* Sorting Widget
 */
Faceted.SortingWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + this.wid + "_widget");
    this.widget.show();
    this.title = jQuery("legend", this.widget).html();
    this.reverse = jQuery("#" + this.wid + "_reversed");
    this.elements = jQuery("option", this.widget);
    this.selected = [];
    this.select = jQuery("#" + this.wid);

    var error = jQuery(".faceted-widget:has(div.faceted-sorting-errors)");
    if (error.length) {
        error.remove();
        jQuery(Faceted.Events).trigger(Faceted.Events.REDRAW);
        return;
    }

    // Handle select change
    jQuery("form", this.widget).on("submit", function () {
        return false;
    });

    var js_widget = this;
    this.select.on("change", function (evt) {
        js_widget.select_change(this, evt);
    });
    this.reverse.on("click", function (evt) {
        js_widget.reverse_change(this, evt);
    });

    // Default value
    var value = this.select.val();
    if (value) {
        this.selected = this.widget.find("option:selected");
        Faceted.Query[this.wid] = [value];

        var reverse = this.reverse.prop("checked");
        if (reverse) {
            Faceted.Query.reversed = "on";
        }
    }

    // Bind events
    jQuery(Faceted.Events).on(Faceted.Events.QUERY_CHANGED, function () {
        js_widget.synchronize();
    });
    jQuery(Faceted.Events).on(Faceted.Events.RESET, function () {
        js_widget.reset();
    });
};

Faceted.SortingWidget.prototype = {
    select_change: function (element) {
        this.do_query(element);
    },

    reverse_change: function (element) {
        this.do_query(element);
    },

    do_query: function (element) {
        if (!element) {
            this.selected = [];
            Faceted.Form.do_query(this.wid, []);
            return;
        }

        var value = null;
        if (jQuery(element).attr("type") == "checkbox") {
            value = element.checked ? "on" : [];
            if (!this.selected.length) {
                Faceted.Query.reversed = value;
                return;
            }
            Faceted.Form.do_query("reversed", value);
            return;
        } else {
            value = jQuery(element).val();
            if (!value) {
                this.selected = [];
                value = [];
            } else {
                this.selected = this.widget.find("option:selected");
            }
            Faceted.Form.do_query(this.wid, value);
            return;
        }
    },

    reset: function (reversed) {
        reversed = reversed ? true : false;
        this.select.val("");
        this.reverse.attr("checked", reversed);
        this.selected = [];
        this.widget.removeClass("faceted-widget-active");
    },

    synchronize: function () {
        var value = Faceted.Query[this.wid];
        var reversed_value = Faceted.Query.reversed;
        if (!reversed_value) {
            reversed_value = false;
        } else if (reversed_value.length == 1 && !reversed_value[0]) {
            /* reversed value is false if == [""] */
            reversed_value = false;
        } else {
            reversed_value = true;
        }
        if (!value) {
            this.reset(reversed_value);
            return;
        }

        var context = this;
        jQuery.each(value, function () {
            var selected = context.widget.find("option:selected");
            if (!selected.length) {
                context.reset(reversed_value);
            } else {
                context.selected = selected;
                context.select.val(value);
                context.reverse.attr("checked", reversed_value);
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
        var span = jQuery('<span class="faceted-sorting-criterion">');
        html.attr("id", "criteria_" + this.wid + "_entries");
        var element = jQuery(this.selected);
        var value = element.val();
        var label = element.html();
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

        if (this.reverse.prop("checked")) {
            var rid = this.reverse.attr("id");
            var rlabel = jQuery("label[for=" + rid + "]").html();
            html.append("<span>(" + rlabel + ")</span>");
        }

        return html;
    },

    criteria_remove: function () {
        this.select.val("");
        this.reverse.attr("checked", false);
        this.do_query();
    },
};

Faceted.initializeSortingWidget = function () {
    jQuery("div.faceted-sorting-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.SortingWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializeSortingWidget);
