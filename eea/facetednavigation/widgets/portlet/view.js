Faceted.PortletWidget = function (wid) {
    this.wid = wid;
    this.widget = jQuery("#" + wid + "_widget");
    this.widget.show();

    jQuery("legend", this.widget).hide();
    jQuery("fieldset", this.widget).css("border", "none");

    jQuery("form", this.widget).on("submit", function () {
        return true;
    });
};

Faceted.initializePortletWidget = function () {
    jQuery("div.faceted-portlet-widget").each(function () {
        var wid = jQuery(this).attr("id");
        wid = wid.split("_")[0];
        Faceted.Widgets[wid] = new Faceted.PortletWidget(wid);
    });
};

// Initialize
jQuery(Faceted.Events).on(Faceted.Events.INITIALIZE, Faceted.initializePortletWidget);
