String.prototype.replaceAt = function(indexStart, indexEnd, replacement) {
    return this.substr(0, indexStart) + replacement + this.substr(indexEnd);
}


function highlight(comment_reference, indexStart, indexEnd) { // https://stackoverflow.com/questions/52743841/find-and-highlight-word-in-text-using-js
  var paragraph = document.getElementById('text');
//  var opar = paragraph.innerHTML;
  var divChildren = paragraph.childNodes;
  $("#text").children().each(function(){
  search = comment_reference.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); //https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex
//  console.log($(this).html())
  var opar = $(this).html();
  var re = new RegExp(search, 'g');
  var m;
  var matches = opar.matchAll(re)
  for (const match of matches) {
//  console.log("offset: "+ match.off)
      if(indexStart > indexEnd){
        var start = indexStart;
        indexStart = indexEnd;
        indexEnd = start;
      }
      console.log(indexStart+':'+typeof indexStart);
      console.log(match.index+':'+typeof match.index);
      console.log(`Found ${match[0]} start=${match.index} end=${match.index + match[0].length} equal=${indexStart==match.index}.`);
      if (indexStart == match.index) {
        var newInnerHTML = opar.replaceAt(indexStart, indexEnd,  `<span class='highlight'>${match[0]}</span>`)
//        var newInnerHTML = opar.replace(re, `<span class='highlight'>$&</span>`);
//        var newInnerHTML = opar.replace(re, `<mark>$&</mark>`);
        $(this).html(newInnerHTML);
//       innerHTML = opar.substring(0,indexStart) + "<span class='highlight'>" + opar.substring(indexStart,indexEnd) + "</span>" + opar.substring(indexEnd);
//       paragraph.innerHTML += innerHTML;
      }
//      else{
//        paragraph.innerHTML += opar;
//      }
    }

  })
  //var search = document.getElementById('typed-text').value;

//  if (search.length > 0)
//    paragraph.innerHTML = opar.replace(re, `<mark>$&</mark>`);
//  else paragraph.innerHTML = opar;
}
// https://stackoverflow.com/questions/51277123/get-character-offsets-of-beginning-and-end-of-selected-text
//document.addEventListener("mouseup",function(){
//    if(window.getSelection)
//    {
//        var selectedtext = window.getSelection().toString();
//        var range = window.getSelection().getRangeAt(0);
//        var content = range.startContainer.textContent;
//        content = content.replace(/(?:\r\n|\r|\n)/g, '');
//        if(range.startContainer.parentElement.tagName=="BODY")
//        {
//            content = content.replace(/^\s*|\s*$/, '');
//        }
//        console.log(content, content.indexOf(selectedtext), content.indexOf(selectedtext)+selectedtext.length)
//    }
//},false);
document.onselectionchange = function() {
    let {anchorNode, anchorOffset, focusNode, focusOffset} = document.getSelection();

//    console.log(`${anchorNode && anchorNode.data}:${anchorOffset}`);
//    console.log(`${focusNode && focusNode.data}:${focusOffset}`);
//    console.log(`${anchorOffset}:${focusOffset}`);
  };

$( document ).ready(function() {
  $(".comment_reference").each(function(){
    comment_reference = $(this).text();
    console.log("comment reference: "+comment_reference);
    text = comment_reference.split('/')[0];
    indexStart = comment_reference.split('/')[1];
    indexEnd = comment_reference.split('/')[2];
    highlight(text, indexStart, indexEnd);
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
    var selectedtext = window.getSelection().toString();
    var range = window.getSelection().getRangeAt(0);
    var content = range.startContainer.textContent;
    content = content.replace(/(?:\r\n|\r|\n)/g, '');
        if(range.startContainer.parentElement.tagName=="BODY")
        {
            content = content.replace(/^\s*|\s*$/, '');
        }
    console.log(content.indexOf(selectedtext), content.indexOf(selectedtext)+selectedtext.length)
    let {anchorNode, anchorOffset, focusNode, focusOffset} = document.getSelection();
    console.log(`${anchorOffset}:${focusOffset}`);
//   $('#id_comment_reference').val(selectedText+'/'+content.indexOf(selectedtext)+'/'+(content.indexOf(selectedtext)+selectedtext.length));
   $('#id_comment_reference').val(selectedText+'/'+anchorOffset+'/'+focusOffset);
  // https://stackoverflow.com/questions/9756941/knowing-the-text-selected-using-mouse-in-javascript
});