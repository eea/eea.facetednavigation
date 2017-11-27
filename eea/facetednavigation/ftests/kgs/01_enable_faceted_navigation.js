/*==============================================================================*/
/* Casper generated Fri Nov 24 2017 17:30:30 GMT+0200 (EET) */
/*==============================================================================*/

var x = require('casper').selectXPath;
casper.options.viewportSize = {width: 1920, height: 974};
casper.options.pageSettings = {
    userName: 'admin',
    password: 'admin'
};
casper.on('page.error', function(msg, trace) {
   this.echo('Error: ' + msg, 'ERROR');
   for(var i=0; i<trace.length; i++) {
       var step = trace[i];
       this.echo('   ' + step.file + ' (line ' + step.line + ')', 'ERROR');
   }
});


var url ;

if (casper.cli.has("url")) {
url = casper.cli.get("url");

casper.echo("Url is " + url);

casper.test.begin('Faceted Navigation Enable', function(test) {
   casper.start("http://" + url + "/Plone/folder_factories");

   casper.waitForSelector("#form-field-folder",
        function success() {
            test.assertExists("#form-field-folder");
            this.click("#form-field-folder");
        },
        function fail() {
            test.assertExists("#form-field-folder");
    });

    casper.waitForSelector("[name='form.button.Add']",
        function success() {
            test.assertExists("[name='form.button.Add']");
            this.click("[name='form.button.Add']");
        },
        function fail() {
            test.assertExists("[name='form.button.Add']");
    });

   casper.waitForSelector("input[name='title']",
       function success() {
           this.sendKeys("input[name='title']", "Faceted");
       },
       function fail() {
           test.assertExists("input[name='title']");
   });

   casper.waitForSelector("[name='form.button.save']",
       function success() {
           test.assertExists("[name='form.button.save']");
           this.click("[name='form.button.save']");
       },
       function fail() {
           test.assertExists("[name='form.button.save']");
   });

   casper.waitForSelector("[id='plone-contentmenu-actions-faceted.enable']",
       function success() {
           test.assertExists("[id='plone-contentmenu-actions-faceted.enable']");
           this.click('#plone-contentmenu-actions dt a');
           this.clickLabel("Enable faceted navigation");

       },
       function fail() {
           test.assertExists("[id='plone-contentmenu-actions-faceted.enable']");
   });

   casper.waitForSelector("#criteria_c1",
       function success() {
           test.assertExists("#criteria_c1");
         },
       function fail() {
           test.assertExists("#criteria_c1");
   });

   casper.then(function() {
          this.captureSelector("kgs_enable_faceted_navigation.png", "html");
   });

   casper.run(function() {test.done();});
});

} else {
    this.echo('Error: No URL given', 'ERROR');
}
