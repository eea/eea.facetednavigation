/* help function which let you have 
   normal independent input element sends values to a
   eea.facetednavigation object the correct way.
   
   How to use it. HTML example:
   
    <h2>Global search on data and maps</h2>
    <form action="find/global" method="get" id="faceted-text-search">
	<input type="text" onkeypress="return disableEnterKey(event)" name="c12">
	<input type="submit" value="Go!" name="search" class="searchButton">
    </form>
   
   c12 = is the parameter id of your text search facet.
    
*/
$(document).ready(function() {

    if ( !$('body').hasClass('section-data-and-maps')) {
        return;
    }

    $('#faceted-text-search input[type=submit]').click(function(e) {
        e.preventDefault();
        var formActionUrl = $('#faceted-text-search').attr('action');
        var searchTerm = $('#faceted-text-search input[type=text]').val();
        var paramId = $('#faceted-text-search input[type=text]').attr('name');
        var url = formActionUrl + '#' + paramId + '=' + searchTerm;
        window.location.href = url;
    });


});

var disableEnterKey = function(e)
{
    var key;
    if(window.event){
        key = window.event.keyCode; //IE
    }else{
        key = e.which; //firefox
    }
    return (key != 13);
};
