/*console.log('Loaded!');
var element=document.getElementById("main-text");
element.innerHTML='new value';
var img=document.getElementById("mardy");
img.onclick=function(){
    var marginLeft=0;
    function moveRight(){
    marginLeft=marginLeft+1;
    img.style.marginLeft=marginLeft+'px';
    }
    var interval =setInterval(moveRight,50);
   // img.style.marginLeft='100px';
};*/ 
//counter code
//random quote genrator
$(document).ready(function() {
     var quote;
    var author;
function getNewQuote(){

  $.ajax({
    url: 'http://api.forismatic.com/api/1.0/',
    jsonp:'jsonp',
    dataType:'jsonp',
    data:{
        method:'getQuote',
        lang:'en',
        format:'jsonp'
    },
    success: function(response){
    console.log(response.quoteText);
    quote=response.quoteText;
    author=response.quoteAuthor;
    var text = quote + ' - ' + author;
    $('#qwe').text(quote);
  }
  });
}
  getNewQuote();
$("#lvie").on('click',function(event){
    event.preventDefault();
getNewQuote();
});
 $("#twto").on('click',function(event){
    event.preventDefault();
    s=quote;
    window.open(('https://twitter.com/intent/tweet?text='+encodeURIComponent(s)));
});

  });


var button=document.getElementById('counter');

button.onclick = function (){
    
     //make a request to counter end point
     var request=new XMLHttpRequest();
     
     //capture the response and store it into a variable
     request.onreadystatechange= function() {
         if(request.readyState === XMLHttpRequest.DONE)
        {
             //take some action
             if(request.status === 200){
                 var counter=request.responseText;
                 var span=document.getElementById('count');
                 span.innerHTML=counter.toString();
                 
               }
        }       
     };
             //not done yet
               //make a request
 request.open('GET', 'http://ankitnau25.imad.hasura-app.io/counter',true);
 request.send(null);
};




//submit name

var submit=document.getElementById('submit_btn');
submit.onclick=function(){
    //make arequest to the server and send a name
    var request=new XMLHttpRequest();
         
         //capture the response and store it into a variable
         request.onreadystatechange= function() {
             if(request.readyState === XMLHttpRequest.DONE)
             {
                     //take some action
                    if(request.status === 200){
                    //captue a list of nmes and render it as list
                    var names = request.responseText;
                    names=JSON.parse(names);
                    var list = '';
                    for(var i=0;i<names.length;i++){
                        list += '<li>' + names[i] + '</li>';
                    }
                    var ul=document.getElementById('namelist');
                    ul.innerHTML=list;
                 }
             }
             //not done yet
         };
 //make a request
  var nameInput = document.getElementById('name');
  var name = nameInput.value;
  request.open('GET', 'http://ankitnau25.imad.hasura-app.io/submit-name?name=' + name,true);
  request.send(null);
};
