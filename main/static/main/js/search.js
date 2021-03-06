$('#search_form').on('click', function (e) {
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
            $('#search_results').empty();
            $.each(data.hits.hits, function() {
                var text = this.highlight.exact;

//                var regExp = /\(([0-9:+]+)\)/;
//                var matches = regExp.exec(this._id);
//                var p = this._id.split("(");
                var p = this._id.replace(/ *\([^)]*\) */g, "");
                var link = '/api/texts/'+p // '/'+$(location).attr('host')+
                console.log(link);
                var output='<li>'+text+'</li><a href="'+link+'">'+p+'</a>';
                $('#search_results').append(output);
            });
        },
        error: function (error) {
            $("#error").show();
            console.log(error);
        }
    });
})