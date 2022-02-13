
var current_url = $("#current_url").value;
//console.log("current_url: "+ current_url)
function getTextSection(){
    $.ajax({
        url: current_url+'.1', //$("form")[0].action,
        type: "GET",
        success: function (data) {
            console.log(data);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

//getTextSection()