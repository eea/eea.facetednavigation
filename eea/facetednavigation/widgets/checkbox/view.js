/* Checkboxes Widget
 */
Faceted.CheckboxesWidget = function (wid) {
    var self = this;
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");
    this.widget.show();
    this.fieldset = jQuery(".widget-fieldset", this.widget);
    this.title = jQuery("legend", this.widget).html();
    this.elements = jQuery("form input[type=checkbox]", this.widget);
    this.maxitems = parseInt(jQuery("span", this.widget).text(), 10);

    this.operatorElem = this.widget.find(".faceted-operator a");
    this.operatorVisible = this.operatorElem.length ? true : false;

    if (this.operatorVisible) {
        this.operator = this.operatorElem.data("value");

        // Handle operator click
        this.operatorElem.on("click", function (evt) {
            evt.preventDefault();
            self.operator_click(this, evt);
        });

        // Update text
        this.operatorElem.text(this.operatorElem.data(this.operator));
    } else {
        this.operator = this.widget.data("operator");
    }

    this.selected = [];

    // Faceted version
    this.version = "";
    var version = jQuery("#faceted-version");
    if (version) {
        this.version = version.text();
    }

    jQuery("form", this.widget).on("submit", function () {
        return false;
    });

    // Handle checkbox click
    this.elements.on("click", function (evt) {
        self.checkbox_click(this, evt);
    });

    // Default values
    var selected = this.widget.find("form input[type=checkbox]:checked");
    if (selected.length) {
        this.selected = selected;
        Faceted.Query[this.wid] = [];
        selected.each(function () {
            Faceted.Query[self.wid].push(jQuery(this).val());
        });
    }

    if (this.operatorVisible) {
        Faceted.Query[self.wid + "-operator"] = self.operator;
    }

    // Handle More/Less buttons click
    if (this.maxitems) {
        this.fieldset.collapsible({
            maxitems: this.maxitems,
            elements: "li:not(.faceted-checkbox-item-zerocount)",
            more: this.widget.data("more"),
            less: this.widget.data("less"),
        });
    }

    // Bind events
    jQuery(Faceted.Events).on(Faceted.Events.QUERY_CHANGED, function () {
        self.synchronize();
    });
    jQuery(Faceted.Events).on(Faceted.Events.RESET, function () {
        self.reset();
    });
    if (this.widget.hasClass("faceted-count")) {
        var sortcountable = this.widget.hasClass("faceted-sortcountable");
        jQuery(Faceted.Events).on(Faceted.Events.QUERY_INITIALIZED, function () {
            self.count(sortcountable);
        });
        jQuery(Faceted.Events).on(Faceted.Events.FORM_DO_QUERY, function (evt, data) {
            if (
                self.operator != "and" &&
                (data.wid == self.wid || data.wid == "b_start")
            ) {
                return;
            }
            self.count(sortcountable);
        });
    }
};

Faceted.CheckboxesWidget.prototype = {
    checkbox_click: function (element) {
        this.do_query(element);
    },

    operator_click: function () {
        var self = this;
        if (self.operator === "or") {
            self.operator = "and";
            self.operatorElem.text(self.operatorElem.data("and"));
        } else {
            self.operator = "or";
            self.operatorElem.text(self.operatorElem.data("or"));
        }
        Faceted.Form.do_query(this.wid + "-operator", self.operator);
    },

    operator_label: function () {
        if (!this.operatorVisible) {
            return "";
        }

        var label = this.widget.find(".faceted-operator label");
        label = label.length ? label.text() : "";
        label += " " + this.operatorElem.data(this.operator);

        return "(" + label + ")";
    },

    do_query: function () {
        this.selected = jQuery("form input[type=checkbox]:checked", this.widget);
        var value = [];
        this.selected.each(function () {
            value.push(jQuery(this).val());
        });
        Faceted.Form.do_query(this.wid, value);
    },

    reset: function () {
        // This is done by form.reset, so do nothing
        this.selected = [];
        this.widget.removeClass("faceted-widget-active");
        jQuery(this.elements).attr("checked", false);
    },

    synchronize: function () {
        this.elements.attr("checked", false);
        var checked = Faceted.Query[this.wid];
        if (checked) {
            jQuery("form input[type=checkbox]", this.widget).val(checked);
            this.selected = jQuery("form input[type=checkbox]:checked", this.widget);
            this.widget.addClass("faceted-widget-active");
        }

        var operator = Faceted.Query[this.wid + "-operator"];
        if (this.operatorVisible && operator) {
            operator = operator[0];
            this.operator = operator;
            this.operatorElem.data("value", operator);
            this.operatorElem.text(this.operatorElem.data(this.operator));
        }
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
        html.append("<span>" + this.title + " " + this.operator_label() + "</span>");
        return html;
    },

    criteria_body: function () {
        if (!this.selected.length) {
            return "";
        }

        var widget = this;
        var html = jQuery("<dd>");
        html.attr("id", "criteria_" + this.wid + "_entries");

        widget.selected.each(function () {
            var span = jQuery('<span class="faceted-checkbox-criterion">');
            var element = jQuery(this);
            var id = element.attr("id");
            var value = element.val();
            var label = jQuery("label[for=" + id + "]", widget.widget);
            var title = label.attr("title");
            var count = label.children("span").text();

            var link = jQuery('<a href="#" class="faceted-remove">remove</a>');
            link.attr("id", "criteria_" + id);
            link.attr("title", "Remove " + title + " filter");
            link.on("click", function () {
                widget.criteria_remove(value, element);
                return false;
            });

            span.append(link);
            jQuery('<span class="title">').text(title).appendTo(span);
            jQuery('<span class="count">').text(count).appendTo(span);
            html.append(span);
        });

        return html;
    },

    criteria_remove: function (value, element) {
        // Remove all
        if (!value) {
            this.element.each((_, e) => (e.checked = false));
        } else {
            element.each((_, e) => (e.checked = false));
        }
        this.do_query();
    },

    count: function (sortcountable) {
        var query = Faceted.SortedQuery();
        query.cid = this.wid;
        if (this.version) {
            query.version = this.version;
        }
        if (this.operator && !query[this.wid + "-operator"]) {
            query[this.wid + "-operator"] = this.operator;
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
        var lis = jQuery("li", context.widget);
        jQuery(lis).each(function () {
            var li = jQuery(this);
            li.removeClass("faceted-checkbox-item-disabled");
            li.removeClass("faceted-checkbox-item-zerocount");
            var input = jQuery("input", li);
            input.unbind();
            var key = input.val();

            var span = jQuery("span", li);
            if (!span.length) {
                var label = jQuery("label", li);
                label.append(" ");
                label.append(jQuery("<span>"));
                span = jQuery("span", li);
            }

            var value = data[key];
            value = value ? value : 0;
            span.text("(" + data[key] + ")");
            if (sortcountable) {
                li.data("count", value);
            }
            if (!value) {
                li.addClass("faceted-checkbox-item-disabled");
                if (context.widget.hasClass("faceted-zero-count-hidden")) {
                    li.addClass("faceted-checkbox-item-zerocount");
                }
                input.attr("disabled", "disabled");
            } else {
                input.attr("disabled", false);
                input.on("click", function (evt) {
                    context.checkbox_click(this, evt);
                });
            }
        });
        if (sortcountable) {
            lis.detach().sort(function (x, y) {
                var a = jQuery(x).data("count");
                var b = jQuery(y).data("count");
                return b - a;
            });
        }
        jQuery("ul", context.widget).append(lis);
        // Update expand/colapse
        context.fieldset.trigger("widget-refresh");
    },
};

Faceted.initializeCheckboxesWidget = function () {
    jQuery("div.faceted-checkboxes-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.CheckboxesWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializeCheckboxesWidget);
