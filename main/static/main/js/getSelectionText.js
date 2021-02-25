String.prototype.replaceAt = function(indexStart, indexEnd, replacement) {
    return this.substr(0, indexStart) + replacement + this.substr(indexEnd);
}
String.prototype.splice = function(idx, rem, str) {
    console.log(this.slice(0, idx));
    console.log(str);
    console.log(this.slice(idx));
    return this.slice(0, idx) + str + this.slice(idx);
};

function highlight(comment_text, indexStart, indexEnd, nodeIndex) { // https://stackoverflow.com/questions/52743841/find-and-highlight-word-in-text-using-js
  var paragraph = document.getElementById('text');
  var divChildren = paragraph.childNodes;
  var indexOfNode = -1;
  $("#text").children().each(function(){
      indexOfNode++;
//      console.log("indexOfNode: "+indexOfNode);
      var opar = $(this).html();
      if (comment_text == "" & indexOfNode==nodeIndex){  //
        var result = opar.splice(indexStart, 0, "<span class='highlight'>&</span>");
        $(this).html(result);
      }else{
        var search = comment_text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); //https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex
        var re = new RegExp(search, 'g');
        var matches = opar.matchAll(re)
        for (const match of matches) {
        //  console.log("offset: "+ match.off)
          if(indexStart > indexEnd){
            var start = indexStart;
            indexStart = indexEnd;
            indexEnd = start;
          }
        //      console.log(indexStart+':'+typeof indexStart);
        //      console.log(match.index+':'+typeof match.index);
        //      console.log(`Found ${match[0]} start=${match.index} end=${match.index + match[0].length} equal=${indexStart==match.index}.`);
          if (indexStart == match.index) {
            var newInnerHTML = opar.replaceAt(indexStart, indexEnd,  `<span class='highlight'>${match[0]}</span>`)
        //        var newInnerHTML = opar.replace(re, `<mark>$&</mark>`);
            $(this).html(newInnerHTML);
          }
        }
      }
  })
}


document.onselectionchange = function() {
    let {anchorNode, anchorOffset, focusNode, focusOffset} = document.getSelection();
  };

$( document ).ready(function() {
  $(".comment_reference").each(function(){
    comment_reference = $(this).text();
    console.log("comment reference: "+comment_reference);
    text = comment_reference.split('/')[0];
    indexStart = comment_reference.split('/')[1];
    indexEnd = comment_reference.split('/')[2];
    nodeIndex = comment_reference.split('/')[3];
    highlight(text, indexStart, indexEnd, nodeIndex);
  })
});

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
//    var selectedtext = window.getSelection().toString();
    var range = window.getSelection().getRangeAt(0);
    var node = range.startContainer.parentNode;
    console.log(node);
    var content = range.startContainer.textContent;
    var parentNode = node.parentNode;
    console.log(parentNode);
    var index = Array.prototype.indexOf.call(parentNode.children, node);
    console.log("index " + index);
//    content = content.replace(/(?:\r\n|\r|\n)/g, '');
//        if(range.startContainer.parentElement.tagName=="BODY")
//        {
//            content = content.replace(/^\s*|\s*$/, '');
//        }

//    if(selectedText != ''){
//        console.log(content.indexOf(selectedtext), content.indexOf(selectedtext)+selectedtext.length)
    let {anchorNode, anchorOffset, focusNode, focusOffset} = document.getSelection();
    console.log(`${anchorOffset}:${focusOffset}`);
    $('#id_comment_reference').val(selectedText+'/'+anchorOffset+'/'+focusOffset+'/'+index);
    var c = document.getElementById("add_comment");
    c.style.display = "block";
    $("#id_url").val(document.URL);
//    }

    // https://stackoverflow.com/questions/9756941/knowing-the-text-selected-using-mouse-in-javascript
});