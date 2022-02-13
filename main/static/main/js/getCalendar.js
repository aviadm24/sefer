$('#getCalendar').on('click', function (e) {
    console.log("calendar: ")
    e.preventDefault()
    var results_tab = document.getElementById("results_tab");
    if (results_tab.style.display !== 'none') {
        results_tab.style.display = 'none';
    }
    else {
        today = new Date();
        if(!sessionStorage['calendarDate']){
            $.ajax({
                url: "https://www.sefaria.org/api/calendars",
                type: "GET",
                success: function (data) {
                    console.log(data)
                    calendarDate = new Date(data.date);
                    sessionStorage.setItem('calendarDate', calendarDate);
                    sessionStorage.setItem('calendar_items', data.calendar_items);
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
        }
        else{
            today = new Date();
            console.log("today: "+today)
            console.log("session: "+sessionStorage.getItem('calendarDate'))
            console.log("today equels: "+today==sessionStorage.getItem('calendarDate'))
            if (today==sessionStorage.getItem('calendarDate') ){
//                var calendar_items = sessionStorage.getItem('calendar_items');
//                $.each(data.calendar_items, function() {
//                    var title = this.title.en;
//                    var heTitle = this.title.he;
//                    var clean_link = this.url.replace(".", " ");
//                    var ref = this.ref;
//                    var link = '/api/texts/'+clean_link;
//                    var link = '/api/texts/'+ref;
//                    var output='<li>'+title+'</li><a href="'+link+'">('+heTitle+')</a>';
//                    results_tab.insertAdjacentHTML('beforeend', output);
//                });
            }
            else{
                results_tab.innerHTML = "";
                $.ajax({
                    url: "https://www.sefaria.org/api/calendars",
                    type: "GET",
                    success: function (data) {
                        console.log(data)
                        calendarDate = new Date(data.date);
                        sessionStorage.setItem('calendarDate', calendarDate);
                        sessionStorage.setItem('calendar_items', data.calendar_items);
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
            }
        }
        results_tab.style.display = 'block';
    }

})