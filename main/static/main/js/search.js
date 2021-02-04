$('#search_form').on('click', function (e) {
    e.preventDefault()
    // Making the AJAX Request
    console.log("search: "+$("#search_word")[0].value)
    $.ajax({
        url: "https://www.sefaria.org/api/search-wrapper", //$("form")[0].action,
        type: "POST",
        dataType: "jsonp",
        data: {
            query: $("#search_word")[0].value,
            type: "text",
        },
        success: function (data) {
            $("#success").show();
            console.log(data);
        },
        error: function (error) {
            $("#error").show();
            console.log(error);
        }
    });
})