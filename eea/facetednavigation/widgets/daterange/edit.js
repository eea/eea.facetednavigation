FacetedEdit.DateRangeWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");

    this.yearRange = jQuery("input[name=calYearRange]", this.widget).val();
    this.start = jQuery("input[name=start]", this.widget);
    this.end = jQuery("input[name=end]", this.widget);
    this.usePloneFormat = jQuery("input[name=usePloneFormat]", this.widget).val();
    this.usePloneFormat = this.usePloneFormat == "True" ? true : false;
    this.dateFormat = jQuery("input[name=dateFormat]", this.widget).val();

    var js_widget = this;
    this.start.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: this.dateFormat,
        yearRange: this.yearRange,
        onSelect: function (date) {
            js_widget.force_range();
            js_widget.set_default(date);
        },
    });

    this.end.datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: this.dateFormat,
        yearRange: this.yearRange,
        onSelect: function (date) {
            js_widget.set_default(date);
        },
    });

    this.start.on("change", function () {
        js_widget.force_range();
        js_widget.set_default(this);
    });

    this.end.on("change", function () {
        js_widget.set_default(this);
    });

    var start = this.start.val();
    if (start) {
        js_widget.force_range();
    }
};

FacetedEdit.DateRangeWidget.prototype = {
    force_range: function () {
        var start_date = this.start.datepicker("getDate");
        if (!start_date) {
            return;
        }
        this.end.datepicker("option", "minDate", start_date);
    },

    set_default: function () {
        var start = this.start.val();
        var end = this.end.val();
        if ((!start && end) || (start && !end)) {
            return;
        }

        var value = "";
        if (start && end) {
            var start_date;
            var end_date;
            if (this.usePloneFormat) {
                start_date = jQuery.datepicker.parseDate(this.dateFormat, start);
                end_date = jQuery.datepicker.parseDate(this.dateFormat, end);
            } else {
                start_date = new Date(start.replace(/-/g, "/"));
                end_date = new Date(end.replace(/-/g, "/"));
            }
            if (end_date < start_date) {
                var msg = "End Date should be greater than Start date";
                jQuery(FacetedEdit.Events).trigger(FacetedEdit.Events.AJAX_STOP, {
                    msg: msg,
                });
                return;
            }
            value = start + "=>" + end;
        }
        var query = {};
        query.redirect = "";
        query.updateCriterion_button = "Save";
        query.cid = this.wid;
        query["faceted." + this.wid + ".default"] = value;

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

FacetedEdit.initializeDateRangeWidget = function () {
    jQuery("div.faceted-daterange-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        FacetedEdit.Widgets[wid] = new FacetedEdit.DateRangeWidget(wid);
    });
};

// Initialize
jQuery(FacetedEdit.Events).on(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeDateRangeWidget
);
