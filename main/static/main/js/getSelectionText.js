
function highlight(comment_reference, index) { // https://stackoverflow.com/questions/52743841/find-and-highlight-word-in-text-using-js
  var paragraph = document.getElementById('text');
  var opar = paragraph.innerHTML;
  //var search = document.getElementById('typed-text').value;
  search = comment_reference.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); //https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex

  var re = new RegExp(search, 'g');
  var m;
  var matches = opar.matchAll(re)
  for (const match of matches) {
    console.log(`Found ${match[0]} start=${match.index} end=${match.index + match[0].length}.`);
      if (index == match.index) {
       innerHTML = opar.substring(0,index) + "<span class='highlight'>" + opar.substring(index,index+text.length) + "</span>" + opar.substring(index + text.length);
       paragraph.innerHTML = innerHTML;
      }
    }

//  if (search.length > 0)
//    paragraph.innerHTML = opar.replace(re, `<mark>$&</mark>`);
//  else paragraph.innerHTML = opar;
}

$( document ).ready(function() {
  $(".comment_reference").each(function(){
    comment_reference = $(this).text();
    console.log("comment reference: "+comment_reference);
    text = comment_reference.split('/')[0];
    index = comment_reference.split('/')[1];
    highlight(text, index);
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
    // To write the selected text into the textarea
   console.log('selected text: '+ selectedText);
   var thisText = $(this).text();
   var start = thisText.indexOf(selectedText);
   console.log("length: " + selectedText.length);
   var end = start + selectedText.length;
   //if (start >= 0 && end >= 0){
        console.log("start: " + start);
        console.log("end: " + end);
    //}
   $('#id_comment_reference').val(selectedText+'/'+start.toString());
  // https://stackoverflow.com/questions/9756941/knowing-the-text-selected-using-mouse-in-javascript
});