function getSelectedText() {

}

$("#text").mouseup(function(){
    var selectedText = '';

    // window.getSelection
    if (window.getSelection) {
        selectedText = window.getSelection();
    }
    // document.getSelection
    else if (document.getSelection) {
        selectedText = document.getSelection();
    }
    // document.selection
    else if (document.selection) {
        selectedText =
        document.selection.createRange().text;
    } else return;
    // To write the selected text into the textarea
   console.log('selected text: '+ selectedText);
   $('#id_comment_reference').val(selectedText);

});