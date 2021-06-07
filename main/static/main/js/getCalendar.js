$('#getCalendar').on('click', function (e) {
    console.log("calendar: ")
    e.preventDefault()
    var results_tab = document.getElementById("results_tab");
    $.ajax({
        url: "https://www.sefaria.org/api/calendars",
        type: "GET",
        success: function (data) {
            console.log(data)
            $.each(data.calendar_items, function() {
                    var title = this.title.en;
                    var heTitle = this.title.he;
                    var clean_link = this.url.replace(".", " ");
                    var ref = this.ref;
                    var link = '/api/texts/'+clean_link;
                    var link = '/api/texts/'+ref;
                    var output='<li>'+title+'</li><a href="'+link+'">('+heTitle+')</a>';
                    results_tab.insertAdjacentHTML('beforeend', output);
                });
        },
        error: function (error) {
            $("#error").show();
            console.log(error);
        }
    });
})