function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function is_user_authenticated(callback){
    $.ajax({
        url: "/is_authenticated/", //$("form")[0].action,
        type: "POST",
//        data: {
//            comment: $("#id_comment")[0].value,
//            url: $("#id_url")[0].value,
//            comment_reference: $("#id_comment_reference")[0].value,
//        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (resp) {
            data = resp;
            callback(data);
        },
        error: function (error) {
            console.log(error);
        }
    });
}


function add_comment(){
    is_user_authenticated(function(data){
        if(data.msg == "true"){
            var c = document.getElementById("add_comment");
            if(c.style.display === "none"){
                c.style.display = "block";
            }else{
                c.style.display = "none";
            }
            $("#id_url").val(document.URL);
        }else{
            window.location = "/accounts/login/";
        }
    });
}


// Setting the Click Event Listener on the Submit Button
$('#add_comment_form').on('click', function (e) {
    e.preventDefault()
    // Making the AJAX Request
    console.log("url: "+$("#id_url")[0].value)
    $.ajax({
        url: "/add_comment/", //$("form")[0].action,
        type: "POST",
        data: {
            comment: $("#id_comment")[0].value,
            url: $("#id_url")[0].value,
            comment_reference: $("#id_comment_reference")[0].value,
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
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


