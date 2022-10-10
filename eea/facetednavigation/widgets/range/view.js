/* Range Widget
 */

Faceted.RangeWidget = function (wid) {
    var js_widget = this;
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");
    this.widget.show();
    this.title = jQuery("legend", this.widget).html();

    this.start = jQuery("input[name=start]", this.widget);
    this.end = jQuery("input[name=end]", this.widget);
    this.selected = [];

    this.invalidRangeMsg = this.widget.data("invalid-range-msg");

    var start = this.start.val();
    var end = this.end.val();
    if (start && end) {
        this.selected = [this.start, this.end];
        Faceted.Query[this.wid] = [start, end];
    }

    // Handle clicks
    jQuery("form", this.widget).on("submit", function () {
        return false;
    });
    var handle = function (evt) {
        js_widget.select_change(this, evt);
    };
    this.start.on("change", handle);
    this.end.on("change", handle);

    // Bind events
    jQuery(Faceted.Events).on(Faceted.Events.QUERY_CHANGED, function () {
        js_widget.synchronize();
    });
    jQuery(Faceted.Events).on(Faceted.Events.RESET, function () {
        js_widget.reset();
    });
};

Faceted.RangeWidget.prototype = {
    select_change: function (element) {
        this.do_query(element);
    },

    do_query: function () {
        var start = this.start.val();
        start = parseFloat(start) || start;
        var end = this.end.val();
        end = parseFloat(end) || end;

        if (!start || !end) {
            this.selected = [];
            return false;
        }

        var value = [this.start.val(), this.end.val()];

        if (end < start) {
            Faceted.Form.raise_error(this.invalidRangeMsg, this.wid + "_errors", []);
        } else {
            this.selected = [this.start, this.end];
            Faceted.Form.clear_errors(this.wid + "_errors", []);
            Faceted.Form.do_query(this.wid, value);
        }
    },

    reset: function () {
        this.selected = [];
        this.widget.removeClass("faceted-widget-active");
        this.start.val("");
        this.end.val("");
    },

    synchronize: function () {
        var value = Faceted.Query[this.wid];
        if (!value) {
            this.reset();
            return false;
        }
        if (!value.length) {
            this.reset();
            return false;
        }
        if (value.length < 2) {
            this.reset();
            return false;
        }

        var start = value[0];
        var end = value[1];

        // Set start, end inputs
        this.start.val(start);
        this.end.val(end);
        this.selected = [this.start, this.end];
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
        var span = jQuery('<span class="faceted-range-criterion">');
        var start = this.start.val();
        var end = this.end.val();

        var label = start + " - " + end;
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

Faceted.initializeRangeWidget = function () {
    jQuery("div.faceted-range-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.RangeWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializeRangeWidget);
