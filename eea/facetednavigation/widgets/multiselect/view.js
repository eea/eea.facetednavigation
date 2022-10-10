/* Select Widget
 */
Faceted.MultiSelectWidget = function (wid) {
    var self = this;
    this.wid = wid;
    this.widget = jQuery("#" + this.wid + "_widget");
    this.widget.show();
    this.title = this.widget.find("legend").html();
    this.elements = this.widget.find("option");
    this.select = jQuery("#" + this.wid);
    this.multiple = this.select.attr("multiple") ? true : false;
    this.placeholder = this.widget.data("placeholder");
    this.closeOnSelect = this.widget.data("closeonselect");
    this.ajax = this.widget.data("ajax");
    this.selected = [];

    if (!this.ajax) {
        this.select.select2({
            placeholder: this.placeholder,
            closeOnSelect: this.closeOnSelect,
            allowClear: true,
        });
    } else {
        this.select.select2({
            placeholder: this.placeholder,
            closeOnSelect: this.closeOnSelect,
            allowClear: true,
            multiple: this.multiple,
            ajax: {
                url: self.ajax,
                dataType: "json",
                data: function (term) {
                    var query = {
                        q: term,
                    };
                    return query;
                },
                results: function (data) {
                    return {
                        results: data.items,
                    };
                },
            },
            initSelection: function (element, callback) {
                var id = jQuery(element).val();
                if (id !== "") {
                    jQuery
                        .ajax(self.ajax + "?wildcard:int=0&q=" + id, {
                            dataType: "json",
                        })
                        .done(function (data) {
                            if (self.multiple) {
                                callback(data.items);
                            } else if (data.items.length) {
                                callback(data.items[0]);
                            }
                        });
                }
            },
        });
    }

    // Faceted operator
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

    this.select.on("select2-close", function (evt) {
        self.select_change(this, evt);
    });

    this.select.on("select2-removed", function (evt) {
        self.select_change(this, evt);
    });

    // Default value
    var value = this.select.val();
    if (value) {
        if (this.ajax) {
            this.selected = this.multiple
                ? this.widget.find('input[type="hidden"]')
                : this.widget.find('input[type="text"]');
        } else {
            this.selected = this.widget.find("option:selected");
        }
        if (this.multiple) {
            Faceted.Query[this.wid] = value;
        } else {
            Faceted.Query[this.wid] = [value];
        }
    }

    if (this.operatorVisible) {
        Faceted.Query[self.wid + "-operator"] = self.operator;
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

Faceted.MultiSelectWidget.prototype = {
    select_change: function (element) {
        if (!jQuery(element).val()) {
            element = null;
        }
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

    do_query: function (element) {
        if (!element) {
            this.selected = [];
            return Faceted.Form.do_query(this.wid, []);
        } else {
            var value = jQuery(element).val();
            if (this.ajax) {
                this.selected = this.multiple
                    ? this.widget.find('input[type="hidden"]')
                    : this.widget.find('input[type="text"]');
            } else {
                this.selected = this.widget.find("option:selected");
            }
            return Faceted.Form.do_query(this.wid, value);
        }
    },

    reset: function () {
        this.select.val(null).trigger("change.select2");
        this.selected = [];
        this.widget.removeClass("faceted-widget-active");
    },

    synchronize: function () {
        var value = Faceted.Query[this.wid];
        if (value) {
            this.select.val(value).trigger("change.select2");
            if (this.ajax) {
                this.selected = this.multiple
                    ? this.widget.find('input[type="hidden"]')
                    : this.widget.find('input[type="text"]');
            } else {
                this.selected = this.widget.find("option:selected");
            }
            this.widget.addClass("faceted-widget-active");
        } else {
            this.reset();
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
        html.append("<span>" + this.title + "</span>");
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
            var span = jQuery('<span class="faceted-multiselect-criterion">');
            var element = jQuery(this);
            var id = element.attr("id");
            var value = element.val();
            var to_remove = value;
            if (!value) {
                value = element.parent().find("a").text();
                to_remove = null;
            }
            var label = element.attr("title") || value;

            var link = jQuery('<a href="#" class="faceted-remove">remove</a>');
            link.attr("id", "criteria_" + id);
            link.attr("title", "Remove " + label + " filter");
            link.on("click", function () {
                widget.criteria_remove(to_remove, element);
                return false;
            });

            span.append(link);
            jQuery("<span>").text(label).appendTo(span);
            html.append(span);
        });

        return html;
    },

    criteria_remove: function (value, element) {
        // Remove all
        if (!value) {
            this.select.val(null).trigger("change.select2");
            this.do_query();
        } else {
            element.attr("selected", false);
            this.select.trigger("change.select2");
            this.do_query(this.select);
        }
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
        var select = jQuery("select", context.widget);
        var options = jQuery("option", context.widget);
        var current_val = select.val();
        jQuery(options).each(function () {
            var option = jQuery(this);
            if (!option.attr("title")) {
                return;
            }
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

Faceted.initializeMultiSelectWidget = function () {
    jQuery("div.faceted-multiselect-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.MultiSelectWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(
    Faceted.Events.INITIALIZE,
    Faceted.initializeMultiSelectWidget
);
