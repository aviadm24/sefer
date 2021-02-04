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