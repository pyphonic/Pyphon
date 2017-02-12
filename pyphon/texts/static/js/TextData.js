// Module for calling the Text api and printing out its results.


'use strict';


function textData(text){
    this.time = text.time;
    this.body = text.body;
    this.sender = text.sender;
 };

textData.allTexts = []

textData.callAPI = function(){
    //Call the Api to grab recent texts
    $.get('/api/texts', function(data,msg,xhr){

        console.log(data);
        textData.allTexts = data.map(function(data,idx,array){
          return new textData(data);
        textData.renderData(textData.allTexts)
        });
    });
};

textData.renderData = function(textsArray){
    textsArray.sort(function(a, b){
      return b.time - a.time;
    });
    $('#past_texts .message').remove();
    

}