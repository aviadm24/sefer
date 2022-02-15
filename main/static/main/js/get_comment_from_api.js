
function func(id){
    console.log("toggle: "+id)
    $('#'+id+'t').toggle();
}

function get_comment_from_api (url_to_commentators, main_text_url, commentaryDivId) {
    window.event.preventDefault();
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
                    console.log("response.error: "+response.error === true)
                    if (response.error) {
                        commentaryDiv.innerHTML='<div style="color:red">לא נמצאו פירושים על הפסקה הזאת</div>'
                    }
                    else {
                        var index = 1
                        console.log("commentary_main_list: "+response.commentary_main_list)
                        for (var commentary_obj of response.commentary_main_list){
                            console.log("name: "+commentary_obj.hebrew_short_name)
//                            commentText = gen_commentary_div(commentary_obj.text_list, commentaryDivId+'-'+commentary_obj.index_title)
//                            console.log("commentText: "+commentText)
                            var $wrapper = $("<div/>", { class: "wrapper", id: commentaryDivId+'-'+index+'t' })
                            for (var text of commentary_obj.text_list){
                                var $inner = $("<p/>", { class: "inner" }),
                                    $text = $("<span/>", { class: "text", html: text });
                                $wrapper.append($inner.append(text));
                                }
                                $wrapper.hide()
                            var $li = $("<li/>", { class: "inner" }),
                                $a = $("<a/>", { id: commentaryDivId+'-'+index, text: commentary_obj.hebrew_short_name, onclick: "func(this.id)" });
                            $li.append($a);
                            $li.append($wrapper);
//                            commentaryDiv.insertAdjacentHTML( 'beforeend', '<li class="" id=""><a href="#" id="'+commentaryDivId+'-'+index+'">'+commentary_obj.hebrew_short_name+'</a>'+commentText+'</li>');
                            commentaryDiv.appendChild($li[0]);
//                            $('#'+commentaryDivId+'-'+index).click(function(){
//                                console.log("toggle: "+commentary_obj.index_title)
//                                var commentaryTextDiv = document.getElementById(commentaryDivId+'-'+commentary_obj.index_title);
//                                if (commentaryTextDiv.style.display !== 'none') {
//                                    commentaryTextDiv.style.display = 'none';
//                                }
//                                else {
//                                    commentaryTextDiv.style.display = 'block';
//                                }
////                                $('#'+commentaryDivId+'-'+commentary_obj.index_title).toggle();
//                            });
                            index++;
                            //                            commentaryDiv.insertAdjacentHTML( 'beforeend', '<li class="" id="">'+comment.sourceHeRef+' - '+comment.he+'</li>');
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

