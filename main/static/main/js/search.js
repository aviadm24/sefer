function openWindow(path, callback /* , arg1 , arg2, ... */){
    var args = Array.prototype.slice.call(arguments, 2); // retrieve the arguments
    var w = window.open(path); // open the new window
    w.addEventListener('load', afterLoadWindow.bind(w, args), false); // listen to the new window's load event
    function afterLoadWindow(/* [arg1,arg2,...], loadEvent */){
        callback.apply(this, arguments[0]); // execute the callbacks, passing the initial arguments (arguments[1] contains the load event)
    }
}

$('#search_form').on('click', function (e) {
    console.log("search: ")
    e.preventDefault()
    // Making the AJAX Request
    console.log("search: "+$("#search_word")[0].value)
    var query ={
      "query": $("#search_word")[0].value,
      "type": "text"
    }
    $.ajax({
        url: "https://www.sefaria.org/api/search-wrapper", //$("form")[0].action,
        type: "POST",
//        dataType: "jsonp",
        data : JSON.stringify(query),
        success: function (data) {
            openWindow("/search_results",function(oldWinDAta){
//                this.alert("Hello "+firstname);
                this.console.log(oldWinDAta)
                var search_results_tab = this.document.getElementById("search_results");
                //search_results_tab.append("test")
                //$('#search_results').empty();
                $.each(oldWinDAta.hits.hits, function() {
                    var text = this.highlight.exact;
                    var p = this._id.replace(/ *\([^)]*\) */g, "");
                    var link = '/api/texts/'+p;
                    var output='<li>'+text+'</li><a href="'+link+'">'+p+'</a>';
                    search_results_tab.insertAdjacentHTML('beforeend', output);
                });
            }, data);

//            $('#search_results').empty();
//            $.each(data.hits.hits, function() {
//                var text = this.highlight.exact;
//                var p = this._id.replace(/ *\([^)]*\) */g, "");
//                var link = '/api/texts/'+p // '/'+$(location).attr('host')+
//                console.log(link);
//                var output='<li>'+text+'</li><a href="'+link+'">'+p+'</a>';
//                $('#search_results').append(output);
//
//            });
        },
        error: function (error) {
            $("#error").show();
            console.log(error);
        }
    });
})