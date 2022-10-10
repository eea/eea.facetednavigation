/* Text Widget
 */
Faceted.TextWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");
    this.widget.show();
    this.title = jQuery("legend", this.widget).html();
    this.selected = [];
    this.button = jQuery("input[type=submit]", this.widget);
    this.input = jQuery("#" + this.wid);
    this.value = "";

    // Handle text change
    var js_widget = this;
    var form = this.widget.find("form");
    form.on("submit", function () {
        js_widget.text_change(js_widget.button);
        return false;
    });

    this.input.on("change", function () {
        form.trigger("submit");
    });

    // Default value
    var value = this.input.val();
    if (value) {
        this.selected = [this.input];
        this.value = value;
        Faceted.Query[this.wid] = [value];
    }

    // Bind events
    jQuery(Faceted.Events).on(Faceted.Events.QUERY_CHANGED, function () {
        js_widget.synchronize();
    });
    jQuery(Faceted.Events).on(Faceted.Events.RESET, function () {
        js_widget.reset();
    });
};

Faceted.TextWidget.prototype = {
    text_change: function (element) {
        if (this.value === this.input.val()) {
            return;
        }

        this.do_query(element);
        jQuery(element).removeClass("submitting");
    },

    do_query: function (element) {
        var value = this.input.val();
        value = value ? [value] : [];

        if (!element) {
            this.selected = [];
            this.value = "";
            return Faceted.Form.do_query(this.wid, []);
        }
        this.selected = [this.input];
        this.value = this.input.val();

        var where = jQuery("input[type=radio]:checked", this.widget);
        where = where.length == 1 ? where.val() : "all";
        if (where == "all") {
            return Faceted.Form.do_query(this.wid, value);
        }

        var current = Faceted.Query[this.wid];
        current = current ? current : [];
        if (value.length && !(value[0] in current)) {
            current.push(value[0]);
        }
        return Faceted.Form.do_query(this.wid, current);
    },

    reset: function () {
        this.selected = [];
        this.value = "";
        jQuery("#" + this.wid).val("");
        this.widget.removeClass("faceted-widget-active");
    },

    synchronize: function () {
        var value = Faceted.Query[this.wid];
        if (!value) {
            this.reset();
            return;
        }

        this.input.val(value);
        this.selected = [this.input];
        this.value = this.input.val();
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

        var widget = this;
        var html = jQuery("<dd>");
        var elements = Faceted.Query[this.wid];
        elements = elements ? elements : [];
        jQuery.each(elements, function () {
            var label = this.toString();
            if (label.length > 0) {
                var span = jQuery('<span class="faceted-text-criterion">');
                var link = jQuery('<a href="#" class="faceted-remove">remove</a>');
                link.attr("id", "criteria_" + widget.wid + "_" + label);
                link.attr("title", "Remove " + label + " filter");
                link.on("click", function () {
                    widget.criteria_remove(label);
                    return false;
                });
                span.append(link);
                jQuery("<span>").text(label).appendTo(span);
                html.append(span);
            }
        });
        return html;
    },

    criteria_remove: function (value) {
        this.input.val("");
        if (!value) {
            this.selected = [];
            this.value = "";
            this.do_query();
            return;
        }
        jQuery("#" + this.wid + "_place_current", this.widget).attr("checked", true);
        var element = jQuery("input[type=text]", this.widget);
        var current = Faceted.Query[this.wid];
        var index = jQuery.inArray(value, current);
        if (index == -1) {
            return;
        }
        current.splice(index, 1);
        Faceted.Query[this.wid] = current;
        this.do_query(element);
    },
};

Faceted.initializeTextWidget = function () {
    jQuery("div.faceted-text-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.TextWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializeTextWidget);
