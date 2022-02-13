


function get_comment_from_api (url_to_commentators, main_text_url, commentaryDivId) {
    //e.preventDefault()
    // Making the AJAX Request
    console.log("commentaryDivId: "+commentaryDivId)
//    commentaryDiv = $('#'+commentaryDivId);
    var commentaryDiv = document.getElementById(commentaryDivId);
    console.log("commentaryDiv: "+commentaryDiv.style)
    if (commentaryDiv.style.display !== 'none') {
        commentaryDiv.style.display = 'none';
    }
    else {
        if (commentaryDiv.innerHTML === "") {
            $.ajax({
                data: {"url":url_to_commentators,
                       "main_text_url": main_text_url}, // get the form data
                url: "/get_comment/",
                // on success
                success: function (response) {
                    console.log(response.commentary)
                    if (response.error == true) {
                        commentaryDiv.append('<div class="" id="">לא נמצאו פירושים על הפסקה הזאת</div>')
                    }
                    else {
                        for (var comment of response.commentary){
//                            commentaryDiv.append('<div class="" id="">'+comment.sourceHeRef+' - </div><div class="" id="">'+comment.he+' - </div>')
                            commentaryDiv.insertAdjacentHTML( 'beforeend', '<li class="" id="">'+comment.sourceHeRef+' - '+comment.he+'</li>');
                        }

                    }

                },
                // on error
                error: function (response) {
                    // alert the error if any error occured
                    console.log(response)
                }
            });
        }
        commentaryDiv.style.display = 'block';
    }


}

